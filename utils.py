from datetime import timedelta
import IPython
import matplotlib.pyplot as plt
import numpy as np


# 日付をfor文に使う関数
def date_range(start, stop, step=timedelta(1)):
    current = start
    while current < stop:
        yield current
        current += step


# データフレームを綺麗に出力する関数
def display(*dfs, head=True):
    for df in dfs:
        IPython.display.display(df.head() if head else df)

# 特徴量重要度を棒グラフでプロットする関数
def plot_feature_importance(df, result_dir):
    n_features = len(df)                              # 特徴量数(説明変数の個数)
    df_plot = df.sort_values('importance')            # df_importanceをプロット用に特徴量重要度を昇順ソート
    f_importance_plot = df_plot['importance'].values  # 特徴量重要度の取得
    plt.figure()
    plt.barh(range(n_features), f_importance_plot, align='center')
    cols_plot = df_plot['feature'].values             # 特徴量の取得
    plt.yticks(np.arange(n_features), cols_plot)      # x軸, y軸の値の設定
    plt.xlabel('Feature importance')                  # x軸のタイトル
    plt.ylabel('Feature')                             # y軸のタイトル
    plt.savefig(f'{result_dir}feature_importance.png')
    plt.close()