import os
import datetime
import argparse
from train import train


def main():
    timestamp = "{0:%Y%m%d-%H%M%S}".format(datetime.datetime.now())  # タイムスタンプ
    result_dir = './result/' + timestamp + '/'  # 結果を出力するディレクトリ名
    os.mkdir(result_dir)  # 結果を出力するディレクトリを作成
    param = vars(args)  # コマンドライン引数を取り込み

    # LightGBMの学習
    train(param, result_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-train', '--train_file', type=str, default='./data/preprocess.csv')
    parser.add_argument('-test', '--test_file', type=str, default='./data/test_preprocess.csv')
    args = parser.parse_args()  # 引数解析
    main()
