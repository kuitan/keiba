import os
import datetime
import argparse
from train import train


def main():
    timestamp = "{0:%Y%m%d-%H%M%S}".format(datetime.datetime.now())  # タイムスタンプ
    result_dir = './result/' + timestamp + '/'  # 結果を出力するディレクトリ名
    os.mkdir(result_dir)  # 結果を出力するディレクトリを作成
    param = vars(args)  # コマンドライン引数を取り込み
    param.update({
        'boosting_type': 'gbdt',
        'class_weight': None,
        'colsample_bytree': 1.0,
        'importance_type': 'split',
        'learning_rate': 0.1,
        'max_depth': -1,  # 決定木の深さを指定 -1
        'min_child_samples': 20,
        'min_child_weight': 0.001,
        'min_split_gain': 0.0,
        'n_estimators': 100,
        'n_jobs': -1,
        'num_leaves': 31,  # 葉の数, max_depthと一緒に調整すると良い 31
        'objective': None,
        'random_state': None,
        'reg_alpha': 0.0,
        'reg_lambda': 0.0,
        'silent': True,
        'subsample': 1.0,
        'subsample_for_bin': 200000,
        'subsample_freq': 0
    })  # 追加パラメータ

    # LightGBMの学習
    train(param, result_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-train', '--train_file', type=str, default='./data/preprocess.csv')
    parser.add_argument('-test', '--test_file', type=str, default='./data/test_preprocess.csv')
    args = parser.parse_args()  # 引数解析
    main()
