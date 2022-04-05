import os
import datetime
import argparse
from train import train
from test_scraping import get_test_data
from preprocess import preprocess


def main():
    timestamp = "{0:%Y%m%d-%H%M%S}".format(datetime.datetime.now())  # タイムスタンプ
    result_dir = './result/' + timestamp + '/'  # 結果を出力するディレクトリ名
    os.mkdir(result_dir)  # 結果を出力するディレクトリを作成
    param = vars(args)  # コマンドライン引数を取り込み
    param.update({
        'train_file': f'{result_dir}preprocess.csv',
        'test_file': f'{result_dir}test_preprocess.csv',
        'test_url': 'https://race.netkeiba.com/race/shutuba.html?race_id=202209020411',
        'date': '20220403',
        'result_dir': result_dir
    })  # 追加パラメータ

    # テストデータを作成
    get_test_data(param)

    # 前処理
    date = param['date']
    preprocess(param, date)

    # modelの学習
    train(param)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', type=str, default='gbm')
    parser.add_argument('-l', '--load', type=str, default=None)
    args = parser.parse_args()  # 引数解析
    main()
