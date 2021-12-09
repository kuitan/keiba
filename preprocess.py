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

    for d in date_range(date(2016, 1, 1), date(2021, 12, 8)):
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
            df['着順'] = rank_list

            # 性齢を性別と年齢に分割
            sex = []
            age = []
            for sexual_age in df['性齢']:
                sex.append(sexual_age[:1])
                age.append(sexual_age[1:])
            del df['性齢']
            df['性別'] = sex
            df['年齢'] = age

            # 性別のone-hot encoding
            categories = {'セ', '牡', '牝'}
            df['性別'] = pd.Categorical(df['性別'], categories=categories)
            df = pd.concat([df, pd.get_dummies(df['性別'], dummy_na=True)], axis=1)
            del df['性別']
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
            df['馬体重'] = horse_weight
            df['馬体重差分'] = horse_weight_difference

            # タイムを1着との差分時間[s]に変換
            dt = []
            df['タイム'] = pd.to_datetime(df['タイム'])
            for rank, time in zip(df['着順'].astype('int'), df['タイム']):
                if rank == 1:
                    time_min = time
                    dt.append(0)
                else:
                    dt.append((time-time_min).seconds)
            del df['タイム']
            df['差分時間'] = dt

            # 天候のone-hot encoding
            categories = {' 晴\xa0', ' 曇\xa0', ' 小雨\xa0', ' 雨\xa0'}
            df['天候'] = pd.Categorical(df['天候'], categories=categories)
            df = pd.concat([df, pd.get_dummies(df['天候'], dummy_na=True)], axis=1)
            del df['天候']
            df = df[df[np.nan] != 1]  # 欠損値を除外
            del df[np.nan]

            # 芝状態のone-hot encoding
            categories = {' 良\xa0', ' 稍重\xa0', ' 重\xa0', ' 不良\xa0'}
            df['芝状態'] = pd.Categorical(df['芝状態'], categories=categories)
            df = pd.concat([df, pd.get_dummies(df['芝状態'], dummy_na=True)], axis=1)
            del df['芝状態']
            df = df[df[np.nan] != 1]  # 欠損値を除外
            del df[np.nan]

            if i == 0:
                df1 = df
            else:
                df2 = df
                df1 = pd.concat([df1, df2])
            i += 1

            # print(df_concat)

        except FileNotFoundError as e:
            print(e)

    # 調教師のidを追加
    df1.insert(0, 'trainer_id', df1['調教師'].apply(lambda x: trainer_dic[x]))
    del df1['調教師']

    # 騎手のidを追加
    df1.insert(0, 'jockey_id', df1['騎手'].apply(lambda x: jockey_dic[x]))
    del df1['騎手']

    # 馬名のidを追加
    df1.insert(0, 'horse_id', df1['馬名'].apply(lambda x: horse_dic[x]))
    del df1['馬名']

    # 不要な属性を削除
    del df1['馬番']
    del df1['着差']
    del df1['発走']

    # カテゴリを調べる
    # categories = set(df1['性別'].unique().tolist())
    # print(categories)

    print(df1)

    # CSVファイルとして出力
    df1.to_csv(f'./data/preprocess.csv')



if __name__ == '__main__':
    preprocess()