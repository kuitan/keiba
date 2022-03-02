from datetime import date
from utils import date_range
import pandas as pd
import numpy as np
import re


def preprocess():
    result_dir = './result/'  # 結果を出力するディレクトリ名
    i = 0
    horse_idx = 0
    jockey_idx = 0
    trainer_idx = 0
    horse_dic = {}
    jockey_dic = {}
    trainer_dic = {}

    for d in date_range(date(2011, 1, 1), date(2022, 2, 25)):
        # dateを使った処理
        d = d.strftime("%Y%m%d")

        try:
            df = pd.read_csv(f'{result_dir}{d}.csv')

            # 馬名，騎手，調教師を辞書化
            for horse_key, jockey_key, trainer_key in zip(df['馬名'], df['騎手'], df['調教師']):
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

            # タイムがNaNの馬を除外
            df = df.dropna(subset=['タイム'])

            # 着順「失格」を除外
            df = df[df['着順'] != '失']

            # 着順の(降)を削除
            rank_list = []
            for rank in df['着順'].astype('str'):
                rank = re.split('[()]', rank)
                rank_list.append(rank[0])
            del df['着順']
            df['order_of_arrival'] = rank_list

            # 性齢を性別と年齢に分割
            sex = []
            age = []
            for sexual_age in df['性齢']:
                sex.append(sexual_age[:1])
                age.append(sexual_age[1:])
            del df['性齢']
            df['sex'] = sex
            df['age'] = age

            # 性別のone-hot encoding
            categories = {'セ', '牡', '牝'}
            df['sex'] = pd.Categorical(df['sex'], categories=categories)
            df = pd.concat([df, pd.get_dummies(df['sex'], dummy_na=True)], axis=1)
            df = df.rename(columns={'セ': 'gelding', '牡': 'male', '牝': 'mare'})
            del df['sex']
            df = df[df[np.nan] != 1]  # 欠損値を除外
            del df[np.nan]

            # 馬体重「計不」を除外
            df = df[df['馬体重'] != '計不']

            # 馬体重を馬体重と馬体重差分に分割
            horse_weight = []
            horse_weight_difference = []
            for weight in df['馬体重']:
                weight_list = re.split('[()]', weight)
                horse_weight.append(weight_list[0])
                horse_weight_difference.append(weight_list[1])
            del df['馬体重']
            df['horse_weight'] = horse_weight
            df['horse_weight_difference'] = horse_weight_difference

            # タイムを1着との差分時間[s]に変換
            dt = []
            df['タイム'] = pd.to_datetime(df['タイム'])
            for rank, time in zip(df['order_of_arrival'].astype('int'), df['タイム']):
                if rank == 1:
                    time_min = time
                    dt.append(0)
                else:
                    dt.append((time-time_min).seconds)
            del df['タイム']
            df['time_difference'] = dt

            # レース名を場と種類と長さに分割
            field = []
            length = []
            race_type = []
            for race in df['レース名']:
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
            del df['レース名']
            df['field'] = field
            df['race_type'] = race_type
            df['length'] = length

            # 場のone-hot encoding
            categories = {'芝', 'ダ', '障'}
            df['field'] = pd.Categorical(df['field'], categories=categories)
            df = pd.concat([df, pd.get_dummies(df['field'], dummy_na=True)], axis=1)
            df = df.rename(columns={'芝': 'turf', 'ダ': 'dirt', '障': 'obstacle'})
            del df['field']
            df = df[df[np.nan] != 1]  # 欠損値を除外
            del df[np.nan]

            # レース種類のone-hot encoding
            categories = {'直線', '右', '左', '芝'}
            df['race_type'] = pd.Categorical(df['race_type'], categories=categories)
            df = pd.concat([df, pd.get_dummies(df['race_type'], dummy_na=True)], axis=1)
            df = df.rename(columns={'直線': 'straight', '右': 'right', '左': 'left', '芝': 'others'})
            del df['race_type']
            df = df[df[np.nan] != 1]  # 欠損値を除外
            del df[np.nan]
            del df['others']  # othersを除外

            # 天候のone-hot encoding
            categories = {' 晴\xa0', ' 曇\xa0', ' 小雨\xa0', ' 雨\xa0'}
            df['天候'] = pd.Categorical(df['天候'], categories=categories)
            df = pd.concat([df, pd.get_dummies(df['天候'], dummy_na=True)], axis=1)
            df = df.rename(columns={' 晴\xa0': 'sunny', ' 曇\xa0': 'cloudy', ' 小雨\xa0': 'light_rain', ' 雨\xa0': 'rain'})
            del df['天候']
            df = df[df[np.nan] != 1]  # 欠損値を除外
            del df[np.nan]

            # 芝状態のone-hot encoding
            categories = {' 良\xa0', ' 稍重\xa0', ' 重\xa0', ' 不良\xa0'}
            df['芝状態'] = pd.Categorical(df['芝状態'], categories=categories)
            df = pd.concat([df, pd.get_dummies(df['芝状態'], dummy_na=True)], axis=1)
            df = df.rename(columns={' 良\xa0': 'good', ' 稍重\xa0': 'slightly_heavy', ' 重\xa0': 'heavy', ' 不良\xa0': 'bad'})
            del df['芝状態']
            df = df[df[np.nan] != 1]  # 欠損値を除外
            del df[np.nan]

            # レース種類からG1,2,3,L,その他を分類
            name_list = []
            for name in df['レース種類'].astype('str'):
                if re.compile('\(G\d\)').search(name):
                    # name_list.append(re.findall('G\d', name)[0])
                    g_name = re.findall('G\d', name)[0]
                    name_list.append(int(re.findall('\d', g_name)[0])*0.1)
                elif re.compile('\(L\)').search(name):
                    # name_list.append('L')
                    name_list.append(0.4)
                else:
                    # name_list.append('other')
                    name_list.append(0.5)
            df['race_title'] = name_list
            del df['レース種類']

            # レース種類のone-hot encoding
            # categories = {'G1', 'G2', 'G3', 'L', 'other'}
            # df['race_title'] = pd.Categorical(df['race_title'], categories=categories)
            # df = pd.concat([df, pd.get_dummies(df['race_title'], dummy_na=True)], axis=1)
            # df = df.rename(columns={'G1': 'G1', 'G2': 'G2', 'G3': 'G3', 'L': 'L', 'other': 'other_races'})
            # del df['race_title']
            # df = df[df[np.nan] != 1]  # 欠損値を除外
            # del df[np.nan]

            if i == 0:
                df1 = df
            else:
                df2 = df
                df1 = pd.concat([df1, df2])
            i += 1

            # print(df_concat)

        except FileNotFoundError as e:
            print(e)

    # テストデータの前処理
    df = pd.read_csv(f'{result_dir}test.csv')

    # 性齢を性別と年齢に分割
    sex = []
    age = []
    for sexual_age in df['性齢']:
        sex.append(sexual_age[:1])
        age.append(sexual_age[1:])
    del df['性齢']
    df['sex'] = sex
    df['age'] = age

    # 性別のone-hot encoding
    categories = {'セ', '牡', '牝'}
    df['sex'] = pd.Categorical(df['sex'], categories=categories)
    df = pd.concat([df, pd.get_dummies(df['sex'], dummy_na=True)], axis=1)
    df = df.rename(columns={'セ': 'gelding', '牡': 'male', '牝': 'mare'})
    del df['sex']
    df = df[df[np.nan] != 1]  # 欠損値を除外
    del df[np.nan]

    # 馬体重を馬体重と馬体重差分に分割
    horse_weight = []
    horse_weight_difference = []
    for weight in df['馬体重']:
        weight_list = re.split('[()]', weight)
        horse_weight.append(weight_list[0])
        horse_weight_difference.append(weight_list[1])
    del df['馬体重']
    df['horse_weight'] = horse_weight
    df['horse_weight_difference'] = horse_weight_difference

    # レース名を場と種類と長さに分割
    field = []
    length = []
    race_type = []
    for race in df['レース名']:
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
    del df['レース名']
    df['field'] = field
    df['race_type'] = race_type
    df['length'] = length

    # 場のone-hot encoding
    categories = {'芝', 'ダ', '障'}
    df['field'] = pd.Categorical(df['field'], categories=categories)
    df = pd.concat([df, pd.get_dummies(df['field'], dummy_na=True)], axis=1)
    df = df.rename(columns={'芝': 'turf', 'ダ': 'dirt', '障': 'obstacle'})
    del df['field']
    df = df[df[np.nan] != 1]  # 欠損値を除外
    del df[np.nan]

    # レース種類のone-hot encoding
    categories = {'直線', '右', '左', '芝'}
    df['race_type'] = pd.Categorical(df['race_type'], categories=categories)
    df = pd.concat([df, pd.get_dummies(df['race_type'], dummy_na=True)], axis=1)
    df = df.rename(columns={'直線': 'straight', '右': 'right', '左': 'left', '芝': 'others'})
    del df['race_type']
    df = df[df[np.nan] != 1]  # 欠損値を除外
    del df[np.nan]
    del df['others']  # othersを除外

    # 天候のone-hot encoding
    categories = {'晴', '曇', '小雨', '雨'}
    df['天候'] = pd.Categorical(df['天候'], categories=categories)
    df = pd.concat([df, pd.get_dummies(df['天候'], dummy_na=True)], axis=1)
    df = df.rename(columns={'晴': 'sunny', '曇': 'cloudy', '小雨': 'light_rain', '雨': 'rain'})
    del df['天候']
    df = df[df[np.nan] != 1]  # 欠損値を除外
    del df[np.nan]

    # 芝状態のone-hot encoding
    categories = {'良', '稍重', '重', '不良'}
    df['芝状態'] = pd.Categorical(df['芝状態'], categories=categories)
    df = pd.concat([df, pd.get_dummies(df['芝状態'], dummy_na=True)], axis=1)
    df = df.rename(columns={'良': 'good', '稍重': 'slightly_heavy', '重': 'heavy', '不良': 'bad'})
    del df['芝状態']
    df = df[df[np.nan] != 1]  # 欠損値を除外
    del df[np.nan]

    # レース種類からG1,2,3,L,その他を分類
    name_list = []
    for name in df['レース種類'].astype('str'):
        if re.compile('G\d').search(name):
            # name_list.append(re.findall('G\d', name)[0])
            name_list.append(int(re.findall('\d', name)[0]) * 0.1)
        elif re.compile('L').search(name):
            # name_list.append('L')
            name_list.append(0.4)
        else:
            # name_list.append('other')
            name_list.append(0.5)
    df['race_title'] = name_list
    del df['レース種類']

    # 調教師のidを追加
    df1.insert(0, 'trainer_id', df1['調教師'].apply(lambda x: trainer_dic[x]))
    # df.insert(0, 'trainer_id', df['調教師'].apply(lambda x: trainer_dic[x]))
    del df1['調教師']
    # del df['調教師']

    # 騎手のidを追加
    df1.insert(0, 'jockey_id', df1['騎手'].apply(lambda x: jockey_dic[x]))
    # df.insert(0, 'jockey_id', df['騎手'].apply(lambda x: jockey_dic[x]))
    del df1['騎手']
    # del df['騎手']

    # 馬名のidを追加
    df1.insert(0, 'horse_id', df1['馬名'].apply(lambda x: horse_dic[x]))
    # df.insert(0, 'horse_id', df['馬名'].apply(lambda x: horse_dic[x]))
    del df1['馬名']
    # del df['馬名']

    # 着順からtargetを作成
    df1.insert(0, 'target', df1['order_of_arrival'].astype('int').apply(lambda x: 1 if x <= 3 else 0))
    del df1['order_of_arrival']

    # 欠損値を除外
    df1 = df1[df1['length'] != '2']  # 欠損値を除外

    # ヘッダー名を変更
    df1 = df1.rename(columns={'枠番': 'frame_num', '斤量': 'weight_to_carry', '単勝': 'win', '人気': 'popular'})

    # 不要な属性を削除
    del df1['馬番']
    del df1['着差']
    del df1['発走']
    del df1['time_difference']
    del df1['popular']

    # カテゴリを調べる
    # categories = set(df1['race_title'].unique().tolist())
    # print(categories)

    # 各列の標準化
    df1 = df1.astype('float64')
    # categories = ['frame_num', 'weight_to_carry', 'win', 'popular', 'age', 'horse_weight', 'horse_weight_difference',
    #               'length']
    categories = ['frame_num', 'weight_to_carry', 'win', 'horse_weight', 'horse_weight_difference']
    for header in categories:
        df1[header] = (df1[header]-df1[header].mean()) / df1[header].std()
    df1['age'] = df1['age'] * 0.1
    df1['length'] = df1['length'] * 0.001

    del df1['horse_weight']
    del df1['horse_weight_difference']

    # idのone-hot encoding
    # categories = list(horse_dic.keys())
    # df1['horse_id'] = pd.Categorical(df1['horse_id'], categories=categories)
    # df1 = pd.concat([df1, pd.get_dummies(df1['horse_id'])], axis=1)
    # del df1['horse_id']
    # categories = list(jockey_dic.keys())
    # df1['jockey_id'] = pd.Categorical(df1['jockey_id'], categories=categories)
    # df1 = pd.concat([df1, pd.get_dummies(df1['jockey_id'])], axis=1)
    # del df1['jockey_id']
    # categories = list(trainer_dic.keys())
    # df1['trainer_id'] = pd.Categorical(df1['trainer_id'], categories=categories)
    # df1 = pd.concat([df1, pd.get_dummies(df1['trainer_id'])], axis=1)
    # del df1['trainer_id']

    print(df1)

    # 欠損値を除外
    # df = df[df['length'] != '2']  # 欠損値を除外

    # ヘッダー名を変更
    # df = df.rename(columns={'枠番': 'frame_num', '斤量': 'weight_to_carry', '単勝': 'win', '人気': 'popular'})

    # 不要な属性を削除
    # del df['馬番']
    # del df['popular']

    # 各列の標準化
    # df = df.astype('float64')
    # # categories = ['frame_num', 'weight_to_carry', 'win', 'popular', 'age', 'horse_weight', 'horse_weight_difference',
    # #               'length']
    # categories = ['frame_num', 'weight_to_carry', 'win', 'horse_weight', 'horse_weight_difference']
    # for header in categories:
    #     df[header] = (df[header] - df[header].mean()) / df[header].std()
    # df['age'] = df['age'] * 0.1
    # df['length'] = df['length'] * 0.001

    # カテゴリを調べる
    # categories = set(df1['race_type'].unique().tolist())
    # print(categories)

    # del df['horse_weight']
    # del df['horse_weight_difference']

    # print(df)

    # 辞書をnpyファイルで出力
    np.save(f'./data/trainer_dic.npy', trainer_dic)
    np.save(f'./data/jockey_dic.npy', jockey_dic)
    np.save(f'./data/horse_dic.npy', horse_dic)
    # np.savetxt(f'./data/horse_dic.txt', horse_name, fmt="%s")
    # np.savetxt(f'./data/jockey_dic.txt', jockey_name, fmt="%s")
    # np.savetxt(f'./data/trainer_dic.txt', trainer_name, fmt="%s")

    # CSVファイルとして出力
    df1.to_csv(f'./data/preprocess.csv', index=False)
    # df.to_csv(f'./data/test_preprocess.csv', index=False)


def test_preprocess():
    result_dir = './result/'  # 結果を出力するディレクトリ名

    df = pd.read_csv(f'{result_dir}test.csv')

    # 辞書の読み取り
    horse_dic = np.load('./data/horse_dic.npy', allow_pickle='TRUE').tolist()
    jockey_dic = np.load('./data/jockey_dic.npy', allow_pickle='TRUE').tolist()
    trainer_dic = np.load('./data/trainer_dic.npy', allow_pickle='TRUE').tolist()

    horse_idx = []
    jockey_idx = []
    trainer_idx = []

    # 既存idの割り振り
    for horse in horse_dic:
        for name in df['馬名']:
            if name == horse:
                horse_idx.append(horse_dic[horse])

    for jockey in jockey_dic:
        for name in df['騎手']:
            if name == jockey:
                jockey_idx.append(jockey_dic[jockey])

    for trainer in trainer_dic:
        for name in df['調教師']:
            if name == trainer:
                trainer_idx.append(trainer_dic[trainer])

    # 調教師のidを追加
    df.insert(0, 'trainer_id', df['調教師'].apply(lambda x: trainer_dic[x]))
    del df['調教師']

    # 騎手のidを追加
    df.insert(0, 'jockey_id', df['騎手'].apply(lambda x: jockey_dic[x]))
    del df['騎手']

    # 馬名のidを追加
    df.insert(0, 'horse_id', df['馬名'].apply(lambda x: horse_dic[x]))
    del df['馬名']

    # 性齢を性別と年齢に分割
    sex = []
    age = []
    for sexual_age in df['性齢']:
        sex.append(sexual_age[:1])
        age.append(sexual_age[1:])
    del df['性齢']
    df['sex'] = sex
    df['age'] = age

    # 性別のone-hot encoding
    categories = {'セ', '牡', '牝'}
    df['sex'] = pd.Categorical(df['sex'], categories=categories)
    df = pd.concat([df, pd.get_dummies(df['sex'], dummy_na=True)], axis=1)
    df = df.rename(columns={'セ': 'gelding', '牡': 'male', '牝': 'mare'})
    del df['sex']
    df = df[df[np.nan] != 1]  # 欠損値を除外
    del df[np.nan]

    # 馬体重を馬体重と馬体重差分に分割
    horse_weight = []
    horse_weight_difference = []
    for weight in df['馬体重']:
        weight_list = re.split('[()]', weight)
        horse_weight.append(weight_list[0])
        horse_weight_difference.append(weight_list[1])
    del df['馬体重']
    df['horse_weight'] = horse_weight
    df['horse_weight_difference'] = horse_weight_difference

    # レース名を場と種類と長さに分割
    field = []
    length = []
    race_type = []
    for race in df['レース名']:
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
    del df['レース名']
    df['field'] = field
    df['race_type'] = race_type
    df['length'] = length

    # 場のone-hot encoding
    categories = {'芝', 'ダ', '障'}
    df['field'] = pd.Categorical(df['field'], categories=categories)
    df = pd.concat([df, pd.get_dummies(df['field'], dummy_na=True)], axis=1)
    df = df.rename(columns={'芝': 'turf', 'ダ': 'dirt', '障': 'obstacle'})
    del df['field']
    df = df[df[np.nan] != 1]  # 欠損値を除外
    del df[np.nan]

    # レース種類のone-hot encoding
    categories = {'直線', '右', '左', '芝'}
    df['race_type'] = pd.Categorical(df['race_type'], categories=categories)
    df = pd.concat([df, pd.get_dummies(df['race_type'], dummy_na=True)], axis=1)
    df = df.rename(columns={'直線': 'straight', '右': 'right', '左': 'left', '芝': 'others'})
    del df['race_type']
    df = df[df[np.nan] != 1]  # 欠損値を除外
    del df[np.nan]
    del df['others']  # othersを除外

    # 天候のone-hot encoding
    categories = {'晴', '曇', '小雨', '雨'}
    df['天候'] = pd.Categorical(df['天候'], categories=categories)
    df = pd.concat([df, pd.get_dummies(df['天候'], dummy_na=True)], axis=1)
    df = df.rename(columns={'晴': 'sunny', '曇': 'cloudy', '小雨': 'light_rain', '雨': 'rain'})
    del df['天候']
    df = df[df[np.nan] != 1]  # 欠損値を除外
    del df[np.nan]

    # 芝状態のone-hot encoding
    categories = {'良', '稍重', '重', '不良'}
    df['芝状態'] = pd.Categorical(df['芝状態'], categories=categories)
    df = pd.concat([df, pd.get_dummies(df['芝状態'], dummy_na=True)], axis=1)
    df = df.rename(columns={'良': 'good', '稍重': 'slightly_heavy', '重': 'heavy', '不良': 'bad'})
    del df['芝状態']
    df = df[df[np.nan] != 1]  # 欠損値を除外
    del df[np.nan]

    # レース種類からG1,2,3,L,その他を分類
    name_list = []
    for name in df['レース種類'].astype('str'):
        if re.compile('G\d').search(name):
            # name_list.append(re.findall('G\d', name)[0])
            name_list.append(int(re.findall('\d', name)[0])*0.1)
        elif re.compile('L').search(name):
            # name_list.append('L')
            name_list.append(0.4)
        else:
            # name_list.append('other')
            name_list.append(0.5)
    df['race_title'] = name_list
    del df['レース種類']

    # レース種類のone-hot encoding
    # categories = {'G1', 'G2', 'G3', 'L', 'other'}
    # df['race_title'] = pd.Categorical(df['race_title'], categories=categories)
    # df = pd.concat([df, pd.get_dummies(df['race_title'], dummy_na=True)], axis=1)
    # df = df.rename(columns={'G1': 'G1', 'G2': 'G2', 'G3': 'G3', 'L': 'L', 'other': 'other_races'})
    # del df['race_title']
    # df = df[df[np.nan] != 1]  # 欠損値を除外
    # del df[np.nan]

    # 欠損値を除外
    df = df[df['length'] != '2']  # 欠損値を除外

    # ヘッダー名を変更
    df = df.rename(columns={'枠番': 'frame_num', '斤量': 'weight_to_carry', '単勝': 'win', '人気': 'popular'})

    # 不要な属性を削除
    del df['馬番']
    del df['popular']

    # 各列の標準化
    df = df.astype('float64')
    # categories = ['frame_num', 'weight_to_carry', 'win', 'popular', 'age', 'horse_weight', 'horse_weight_difference',
    #               'length']
    categories = ['frame_num', 'weight_to_carry', 'win', 'horse_weight', 'horse_weight_difference']
    for header in categories:
        df[header] = (df[header]-df[header].mean()) / df[header].std()
    df['age'] = df['age'] * 0.1
    df['length'] = df['length']*0.001

    # カテゴリを調べる
    # categories = set(df1['race_type'].unique().tolist())
    # print(categories)

    del df['horse_weight']
    del df['horse_weight_difference']

    print(df)

    # CSVファイルとして出力
    df.to_csv(f'./data/test_preprocess.csv', index=False)


if __name__ == '__main__':
    preprocess()
    test_preprocess()