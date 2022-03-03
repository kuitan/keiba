import pymysql.cursors
import pandas as pd
import numpy as np
import re
from tqdm import tqdm


def get_sql():
    '''
    MySQLからデータを抽出し，DataFrameで出力する関数
    :return: df
    '''

    connection = pymysql.connect(
        user='kkuriyama',
        passwd='kuitan812',
        host='localhost',  # 接続先DBのホスト名或いはIPに書き換えてください。
        db='my_keiba_db',
        local_infile=1  # csvインポートを許可
    )
    cursor = connection.cursor()

    # ヘッダーを取得
    SQL = """
          DESCRIBE race_table;
          """
    cursor.execute(SQL)

    columns_list = []
    for column in cursor.fetchall():
        columns_list.append(column[0])

    # データベースの中身を取得
    SQL = """
          SELECT * FROM race_table;
          """.format(columns=','.join(['`{}`'.format(line) for line in columns_list]))
    cursor.execute(SQL)

    df = pd.read_sql(SQL, connection)

    return df


def preprocess():
    # progress barを設定
    bar = tqdm(total=100)
    bar.set_description('Progress rate')

    pd.set_option('display.max_columns', 100)

    df = get_sql()

    # 不要な属性を削除
    del df['time']
    del df['time_difference']
    del df['start_time']

    # print(df.head())

    result_dir = './result/'  # 結果を出力するディレクトリ名
    horse_idx = 0
    jockey_idx = 0
    trainer_idx = 0
    horse_dic = {}
    jockey_dic = {}
    trainer_dic = {}

    # 欠損値を除外
    df = df.dropna()

    # 着順「失格，中止，除外」を除外
    df = df[df['order_of_arrival'] != '失']
    df = df[df['order_of_arrival'] != '中']
    df = df[df['order_of_arrival'] != '除']

    # テストデータの読み込みと結合
    test_df = pd.read_csv(f'{result_dir}test.csv')
    test_df.insert(0, 'order_of_arrival', 'test')
    df = pd.concat([df, test_df])

    # 辞書を作成
    for horse_key, jockey_key, trainer_key in zip(df['horse_name'], df['jockey'], df['trainer']):
        if horse_key in horse_dic.keys():
            pass
        else:
            horse_dic[horse_key] = horse_idx
            horse_idx += 1

        if jockey_key in jockey_dic.keys():
            pass
        else:
            jockey_dic[jockey_key] = jockey_idx
            jockey_idx += 1

        if trainer_key in trainer_dic.keys():
            pass
        else:
            trainer_dic[trainer_key] = trainer_idx
            trainer_idx += 1

    bar.update(10)

    # 着順の(降)を削除
    rank_list = []
    for rank in df['order_of_arrival']:
        if rank == 'test':
            rank_list.append('test')
        else:
            rank = re.split('[()]', rank)
            rank_list.append(rank[0])
    del df['order_of_arrival']
    df['order_of_arrival'] = rank_list

    bar.update(10)

    # 性齢を性別と年齢に分割
    sex = []
    age = []
    for sexual_age in df['sex_age']:
        sex.append(sexual_age[:1])
        age.append(sexual_age[1:])
    del df['sex_age']
    df['sex'] = sex
    df['age'] = age

    bar.update(10)

    # 性別のone-hot encoding
    categories = {'セ', '牡', '牝'}
    df['sex'] = pd.Categorical(df['sex'], categories=categories)
    df = pd.concat([df, pd.get_dummies(df['sex'], drop_first=True)], axis=1)
    df = df.rename(columns={'セ': 'gelding', '牡': 'male', '牝': 'mare'})
    del df['sex']

    # 馬体重「計不」を除外
    df = df[df['horse_weight'] != '計不']

    # 馬体重を馬体重と馬体重差分に分割
    horse_weight_list = []
    horse_weight_difference_list = []
    for weight in df['horse_weight']:
        weight_list = re.split('[()]', weight)
        horse_weight_list.append(weight_list[0])
        horse_weight_difference_list.append(weight_list[1])
    del df['horse_weight']
    df['horse_weight'] = horse_weight_list
    df['horse_weight_difference'] = horse_weight_difference_list

    bar.update(10)

    # レース名を場と種類と長さに分割
    field = []
    length = []
    race_type = []
    for race in df['race_name']:
        field.append(race[:1])
        length_list = re.split('[^0-9]', race)
        race_type_list = re.split('[0-9]', race)
        race_type_list = race_type_list[0].split()
        race_type.append(race_type_list[0][1:])
        count = 0
        tmp_list = []
        while count < len(length_list):
            if length_list[count] != '':
                tmp_list.append(length_list[count])
            count += 1
        length.append(tmp_list[0])
    del df['race_name']
    df['field'] = field
    df['type'] = race_type
    df['length'] = length

    bar.update(10)

    # 場のone-hot encoding
    categories = {'芝', 'ダ', '障'}
    df['field'] = pd.Categorical(df['field'], categories=categories)
    df = pd.concat([df, pd.get_dummies(df['field'], drop_first=True)], axis=1)
    df = df.rename(columns={'芝': 'turf', 'ダ': 'dirt', '障': 'obstacle'})
    del df['field']

    # レース種類のone-hot encoding
    categories = {'直線', '右', '左', '芝'}
    df['type'] = pd.Categorical(df['type'], categories=categories)
    df = pd.concat([df, pd.get_dummies(df['type'])], axis=1)
    df = df.rename(columns={'直線': 'straight', '右': 'right', '左': 'left', '芝': 'others'})
    del df['others']  # othersを除外
    del df['type']

    # 天候のone-hot encoding
    df = df.replace(' 晴\xa0', '晴')
    df = df.replace(' 曇\xa0', '曇')
    df = df.replace(' 小雨\xa0', '小雨')
    df = df.replace(' 雨\xa0', '雨')
    categories = {'晴', '曇', '小雨', '雨'}
    df['weather'] = pd.Categorical(df['weather'], categories=categories)
    df = pd.concat([df, pd.get_dummies(df['weather'], drop_first=True)], axis=1)
    df = df.rename(columns={'晴': 'sunny', '曇': 'cloudy', '小雨': 'light_rain', '雨': 'rain'})
    del df['weather']

    bar.update(10)

    # 芝状態のone-hot encoding
    df = df.replace(' 良\xa0', '良')
    df = df.replace(' 稍重\xa0', '稍重')
    df = df.replace(' 重\xa0', '重')
    df = df.replace(' 不良\xa0', '不良')
    categories = {'良', '稍重', '重', '不良'}
    df['race_cond'] = pd.Categorical(df['race_cond'], categories=categories)
    df = pd.concat([df, pd.get_dummies(df['race_cond'], drop_first=True)], axis=1)
    df = df.rename(columns={'良': 'good', '稍重': 'slightly_heavy', '重': 'heavy', '不良': 'bad'})
    del df['race_cond']

    bar.update(10)

    # レース種類からG1,2,3,L,その他を分類
    name_list = []
    for rank, name in zip(df['order_of_arrival'], df['race_type']):
        if rank == 'test':
            name_list.append(name)
        else:
            if re.compile('G\d').search(name):
                name_list.append(re.findall('G\d', name)[0])
            elif re.compile('L').search(name):
                name_list.append('L')
            else:
                name_list.append('other_races')
    df['race_title'] = name_list
    del df['race_type']

    bar.update(10)

    # レース種類のone-hot encoding
    categories = {'G1', 'G2', 'G3', 'L', 'other_races'}
    df['race_title'] = pd.Categorical(df['race_title'], categories=categories)
    df = pd.concat([df, pd.get_dummies(df['race_title'], drop_first=True)], axis=1)
    del df['race_title']

    # 調教師のidを追加
    df.insert(0, 'trainer_id', df['trainer'].apply(lambda x: trainer_dic[x]))
    del df['trainer']

    # 騎手のidを追加
    df.insert(0, 'jockey_id', df['jockey'].apply(lambda x: jockey_dic[x]))
    del df['jockey']

    # 馬名のidを追加
    df.insert(0, 'horse_id', df['horse_name'].apply(lambda x: horse_dic[x]))
    del df['horse_name']

    bar.update(10)

    # 欠損値を除外
    df = df[df['length'] != '2']  # 欠損値を除外

    # 不要な属性を削除
    del df['horse_num']
    del df['popular']

    # 標準化
    df['age'] = df['age'].astype('float64')
    df['horse_weight'] = df['horse_weight'].astype('float64')
    df['horse_weight_difference'] = df['horse_weight_difference'].astype('float64')
    df['length'] = df['length'].astype('float64')
    categories = ['frame_num', 'age', 'weight_to_carry', 'win', 'horse_weight', 'horse_weight_difference', 'length']
    for header in categories:
        df[header] = (df[header] - df[header].mean()) / df[header].std()

    bar.update(10)

    del df['horse_weight']
    del df['horse_weight_difference']

    # テストデータと訓練データを分割
    train_df = df.query('order_of_arrival != "test"')
    test_df = df.query('order_of_arrival == "test"')

    # 着順からtargetを作成
    train_df.insert(0, 'target', train_df['order_of_arrival'].astype('int').apply(lambda x: 1 if x <= 3 else 0))
    del train_df['order_of_arrival']
    del test_df['order_of_arrival']

    # floatに変換
    # train_df = train_df.astype('float64')
    # test_df = test_df.astype('float64')

    bar.update(10)

    print('\n')
    print('Progress Finish!')

    print(test_df.head())

    # csvで出力
    train_df.to_csv(f'./data/preprocess.csv', index=False)
    test_df.to_csv(f'./data/test_preprocess.csv', index=False)


if __name__ == '__main__':
    preprocess()