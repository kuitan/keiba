import os
import argparse
from preprocess import preprocess, get_race_list, get_race_date
from train import train
import datetime
from utils import bet_simulation
import matplotlib.pyplot as plt
import numpy as np


def main():
    timestamp = "{0:%Y%m%d-%H%M%S}".format(datetime.datetime.now())  # タイムスタンプ
    result_dir = './result/' + timestamp + '/'  # 結果を出力するディレクトリ名
    os.mkdir(result_dir)  # 結果を出力するディレクトリを作成
    param = vars(args)  # コマンドライン引数を取り込み
    param.update({
        'train_file': f'{result_dir}preprocess.csv',
        'test_file': f'{result_dir}test_preprocess.csv',
        'result_dir': result_dir
    })  # 追加パラメータ

    # メインレースのリストを取得
    # 指定した日付以降のレースリストを作成(G1~G3)
    main_race_list = get_race_list(date='20210101')

    # 所持金
    top_wallet = 0
    box_wallet = 0
    form_wallet = 0
    top_wallet_list = []
    box_wallet_list = []
    form_wallet_list = []

    for i, race in enumerate(main_race_list):
        # raceの日付を取得
        d = get_race_date(race)
        d = d.strftime("%Y%m%d")
        # 前処理
        triple, refund = preprocess(param, d, race=race)
        # テストデータが空でない場合
        if triple is not None:
            # modelの学習
            bet_top_list, bet_box_list, bet_form_list = train(param)
            # 馬券を買って的中しているか判定
            top_money, top_refund, box_money, box_refund, form_money, form_refund \
                = bet_simulation(triple, refund, bet_top_list, bet_box_list, bet_form_list)
            # 所持金を計算
            top_wallet = top_wallet - top_money + top_refund
            top_wallet_list.append(top_wallet)
            print(f'所持金: {top_wallet}円: 上位3つの三連複を買う場合')
            box_wallet = box_wallet - box_money + box_refund
            box_wallet_list.append(box_wallet)
            print(f'所持金: {box_wallet}円: 上位5つの三連複をボックスで買う場合')
            form_wallet = form_wallet - form_money + form_refund
            form_wallet_list.append(form_wallet)
            print(f'所持金: {form_wallet}円: 上位5つの三連複をフォーメーションで買う場合')

        print(f'{i+1} / {len(main_race_list)}')

    # 可視化
    plt.figure()
    plt.plot(np.arange(len(top_wallet_list)), top_wallet_list, label='top_triple')
    plt.plot(np.arange(len(box_wallet_list)), box_wallet_list, label='box_triple')
    plt.plot(np.arange(len(form_wallet_list)), form_wallet_list, label='form_triple')
    plt.xlabel('race num')
    plt.ylabel('wallet [yen]')
    plt.legend()
    plt.savefig(f'{result_dir}wallet.png')
    plt.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', type=str, default='gbm')
    parser.add_argument('-l', '--load', type=str, default=None)
    args = parser.parse_args()  # 引数解析
    main()
