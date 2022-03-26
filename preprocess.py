import pymysql.cursors
import pandas as pd
import re
from tqdm import tqdm


def get_sql(date, later=False, race=None):
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

    if race is not None:
        SQL = """
              SELECT * FROM race_table
              WHERE race_type = '{}';
              """.format(race, columns=','.join(['`{}`'.format(line) for line in columns_list]))
    else:
        if later:
            # データベースの中身を取得
            SQL = """
                  SELECT * FROM race_table
                  WHERE date > {};
                  """.format(date, columns=','.join(['`{}`'.format(line) for line in columns_list]))
        else:
            # データベースの中身を取得
            SQL = """
                  SELECT * FROM race_table
                  WHERE date < {};
                  """.format(date, columns=','.join(['`{}`'.format(line) for line in columns_list]))
    cursor.execute(SQL)

    df = pd.read_sql(SQL, connection)

    return df


def label_encoder(df, columns):
    for col in columns:
        df[col] = df[col].astype('category')
        df.insert(0, col+'_enc', df[col].cat.codes)
        del df[col]

    return df


def preprocess(param, date, race=None):
    # progress barを設定
    bar = tqdm(total=100)
    bar.set_description('Progress rate')

    pd.set_option('display.max_columns', 100)

    train_file = param['train_file']
    test_file = param['test_file']
    result_dir = param['result_dir']

    df = get_sql(date)

    # 不要な属性を削除
    del df['time']
    del df['time_difference']
    del df['start_time']
    del df['date']
    del df['triple']
    del df['refund']

    # 欠損値を除外
    df = df.dropna()

    # 着順「失格，中止，除外」を除外
    df = df[df['order_of_arrival'] != '失']
    df = df[df['order_of_arrival'] != '中']
    df = df[df['order_of_arrival'] != '除']

    # テストデータの読み込みと結合
    if race is not None:
        test_df = get_sql(date, race=race)
        # テストデータが空の時
        if df.empty:
            triple_list = None
            refund = None
            return triple_list, refund
        triple = test_df['triple'].iat[0]
        refund = test_df['refund'].iat[0]
        del test_df['order_of_arrival']
        del test_df['time']
        del test_df['time_difference']
        del test_df['start_time']
        del test_df['date']
        del test_df['triple']
        del test_df['refund']
        test_df.insert(0, 'order_of_arrival', 'test')
        df = pd.concat([df, test_df])
    else:
        test_df = pd.read_csv(f'{result_dir}test.csv')
        test_df.insert(0, 'order_of_arrival', 'test')
        df = pd.concat([df, test_df])

    # Label Encoding
    df = label_encoder(df, columns=['trainer_id', 'jockey_id', 'horse_id'])

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
    for race_name in df['race_name']:
        field.append(race_name[:1])
        length_list = re.split('[^0-9]', race_name)
        race_type_list = re.split('[0-9]', race_name)
        race_type_list = race_type_list[0].split()
        race_type.append(race_type_list[0][1:])
        count = 0
        tmp_list = []
        while count < len(length_list):
            if length_list[count] != '':
                tmp_list.append(length_list[count])
            count += 1
        if '2周' in race_name:
            length.append(tmp_list[1])
        else:
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

    bar.update(10)

    # 欠損値を除外
    df = df[df['length'] != '2']  # 欠損値を除外

    # 不要な属性を削除
    del df['horse_num']
    del df['popular']
    del df['horse_name']
    del df['jockey']
    del df['trainer']

    # 標準化
    df['age'] = df['age'].astype('float64')
    df['horse_weight'] = df['horse_weight'].astype('float64')
    df['horse_weight_difference'] = df['horse_weight_difference'].astype('float64')
    df['length'] = df['length'].astype('float64')
    categories = ['frame_num', 'age', 'weight_to_carry', 'win', 'horse_weight', 'horse_weight_difference', 'length']
    for header in categories:
        df[header] = (df[header] - df[header].mean()) / df[header].std()

    bar.update(10)

    # 馬体重を削除
    # del df['horse_weight']
    # del df['horse_weight_difference']

    # テストデータと訓練データを分割
    train_df = df.query('order_of_arrival != "test"')
    test_df = df.query('order_of_arrival == "test"')

    # 着順からtargetを作成
    train_df.insert(0, 'target', train_df['order_of_arrival'].astype('int').apply(lambda x: 1 if x <= 3 else 0))
    del train_df['order_of_arrival']
    del test_df['order_of_arrival']
    
    # オッズを削除
    del train_df['win']
    del test_df['win']

    bar.update(10)

    print('\n')
    print('Progress Finish!')

    print(test_df.head())

    # csvで出力
    train_df.to_csv(train_file, index=False)
    test_df.to_csv(test_file, index=False)

    # 三連複の払い戻し
    if race is not None:
        triple_list = triple.replace(' - ', ' ').split(' ')
        triple_list = list(map(int, triple_list))
    else:
        triple_list = None
        refund = None

    return triple_list, refund


def get_race_list(date):
    pd.set_option('display.max_columns', 100)

    df = get_sql(date, later=True)
    # 欠損値を除外
    df = df.dropna()

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

    # レース種類のone-hot encoding
    categories = {'G1', 'G2', 'G3', 'L', 'other_races'}
    df['race_title'] = pd.Categorical(df['race_title'], categories=categories)
    df = pd.concat([df, pd.get_dummies(df['race_title'])], axis=1)

    df = df.query('G1 == 1 or G2 == 1 or G3 == 1')

    categories = set(df['race_type'].unique().tolist())
    # print(categories)

    return categories


def get_race_date(race):
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
          SELECT * FROM race_table
          WHERE race_type = '{}';
          """.format(race, columns=','.join(['`{}`'.format(line) for line in columns_list]))
    cursor.execute(SQL)

    df = pd.read_sql(SQL, connection)

    # 日付を取得
    date = df['date'].iat[0]
    # print(date)

    return date


if __name__ == '__main__':
    date = '20220325'  # 今日の日付
    preprocess(date)