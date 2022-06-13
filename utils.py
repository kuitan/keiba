from datetime import timedelta
import IPython
import matplotlib.pyplot as plt
import numpy as np
import torch


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


def get_device():
    """
    実行環境のデバイス(GPU or CPU) を取得
    :return: デバイス (Device)
    """
    if torch.cuda.is_available():
        device = torch.device('cuda')
    else:
        device = torch.device('cpu')
    return device


def bet_simulation(triple, triple_refund, wide, wide_refund, bet_top_list, bet_box_list, bet_form_list,
                   bet_top_wide_list, bet_box_wide_list):

    print(f'結果[ 1着: {triple[0]}, 2着: {triple[1]}, 3着: {triple[2]}]')

    # 上位3つの三連複を買う場合
    # 収出
    top_hit = False
    top_money = 100
    top_refund = 0
    count = 0
    for bet_top in bet_top_list:
        if bet_top in triple:
            count += 1
        if count == 3:
            top_hit = True
            print(f'的中! 払い戻し: {triple_refund}')
    # 的中の場合
    if top_hit:
        top_refund = triple_refund

    # 上位5つの三連複をボックスで買う場合
    # 収出
    box_hit = False
    box_money = len(bet_box_list) * 100
    box_refund = 0
    for bet_box in bet_box_list:
        count = 0
        for bet in bet_box:
            if bet in triple:
                count += 1
            if count == 3:
                box_hit = True
                print(f'的中! 払い戻し: {triple_refund}')
    # 的中の場合
    if box_hit:
        box_refund = triple_refund

    # 上位5つの三連複をフォーメーションで買う場合
    # 収出
    form_hit = False
    form_money = len(bet_form_list) * 100
    form_refund = 0
    for bet_form in bet_form_list:
        count = 0
        for bet in bet_form:
            if bet in triple:
                count += 1
            if count == 3:
                form_hit = True
                print(f'的中! 払い戻し: {triple_refund}')
    # 的中の場合
    if form_hit:
        form_refund = triple_refund

    # 上位2つのワイドを買う場合
    # 収出
    top_wide_money = 100
    top_wide_refund = 0
    if not bet_top_wide_list:  # listが空のとき，馬券は買わない
        top_wide_money = 0
    else:
        for i, w in enumerate(wide):
            count = 0
            for bet_top_wide in bet_top_wide_list:
                if bet_top_wide in w:
                    count += 1
                if count == 2:
                    # 的中の場合
                    print(f'的中! 払い戻し: {wide_refund[i]}')
                    top_wide_refund = wide_refund[i]

    # 上位3つのワイドをボックスで買う場合
    # 収出
    box_wide_money = len(bet_box_wide_list) * 100
    box_wide_refund = 0
    for i, w in enumerate(wide):
        for bet_box_wide in bet_box_wide_list:
            count = 0
            for bet_wide in bet_box_wide:
                if bet_wide in w:
                    count += 1
                if count == 2:
                    # 的中の場合
                    print(f'的中! 払い戻し: {wide_refund[i]}')
                    box_wide_refund += wide_refund[i]

    return top_money, top_refund, box_money, box_refund, form_money, form_refund, top_wide_money, top_wide_refund,\
           box_wide_money, box_wide_refund
