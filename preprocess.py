from datetime import date
from utils import date_range
import pandas as pd
import numpy as np


def preprocess():
    result_dir = './result/'  # 結果を出力するディレクトリ名
    i = 0
    idx = 0
    dic = {}

    for d in date_range(date(2016, 1, 1), date(2021, 12, 8)):
        # dateを使った処理
        d = d.strftime("%Y%m%d")

        try:
            df = pd.read_csv(f'{result_dir}{d}.csv')

            # 馬名を辞書化
            for key in df['馬名']:
                if key in dic.keys():
                    pass
                else:
                    dic[key] = idx
                    idx += 1

            # 天候のone-hot encoding
            categories = {' 晴\xa0', ' 曇\xa0', ' 小雨\xa0', ' 雨\xa0'}
            df['天候'] = pd.Categorical(df['天候'], categories=categories)
            df_concat = pd.concat([df, pd.get_dummies(df['天候'], dummy_na=True)], axis=1)
            del df_concat['天候']
            df_concat = df_concat[df_concat[np.nan] != 1]  # 欠損値を除外
            del df_concat[np.nan]

            # 芝状態のone-hot encoding
            categories = {' 良\xa0', ' 稍重\xa0', ' 重\xa0', ' 不良\xa0'}
            df_concat['芝状態'] = pd.Categorical(df_concat['芝状態'], categories=categories)
            df_concat = pd.concat([df_concat, pd.get_dummies(df_concat['芝状態'], dummy_na=True)], axis=1)
            del df_concat['芝状態']
            df_concat = df_concat[df_concat[np.nan] != 1]  # 欠損値を除外
            del df_concat[np.nan]

            if i == 0:
                df1 = df_concat
            else:
                df2 = df_concat
                df1 = pd.concat([df1, df2])
            i += 1

            # print(df_concat)

        except FileNotFoundError as e:
            print(e)

    # 馬名のidを追加
    df1.insert(0, 'id', df1['馬名'].apply(lambda x: dic[x]))
    del df_concat['馬名']

    print(df1)

    # CSVファイルとして出力
    df1.to_csv(f'./data/preprocess.csv')



if __name__ == '__main__':
    preprocess()