import optuna
import os
import lightgbm as lgb
import argparse
import datetime
import json
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

def lgb_trial(trial):
    param = vars(args)  # コマンドライン引数を取り込み
    param.update({
        'objective': 'binary',
        'metric': trial.suggest_categorical('metric', ['binary_error', "binary_logloss"]),
        'lambda_l1': trial.suggest_loguniform('lambda_l1', 1e-8, 10.0),
        'lambda_l2': trial.suggest_loguniform('lambda_l2', 1e-8, 10.0),
        'num_leaves': trial.suggest_int('num_leaves', 2, 256),
        'feature_fraction': trial.suggest_uniform('feature_fraction', 0.4, 1.0),
        'bagging_fraction': trial.suggest_uniform('bagging_fraction', 0.4, 1.0),
        'bagging_freq': trial.suggest_int('bagging_freq', 1, 7),
        'min_child_samples': trial.suggest_int('min_child_samples', 5, 100),
    })  # 追加パラメータ

    train_file = param['train_file']

    # keibaデータセットの読み込み
    df = pd.read_csv(f'{train_file}')

    # 説明変数,目的変数
    x = df.drop('target', axis=1).values  # 説明変数(target以外の特徴量)
    y = df['target'].values  # 目的変数(target)

    # トレーニングデータ,テストデータの分割
    x_train, x_valid, y_train, y_valid = train_test_split(x, y, test_size=0.20, random_state=0)

    # 学習に使用するデータを設定
    lgb_train = lgb.Dataset(x_train, y_train)
    lgb_eval = lgb.Dataset(x_valid, y_valid, reference=lgb_train)

    # モデルの学習
    model = lgb.train(param, train_set=lgb_train, valid_sets=lgb_eval)

    # 評価データのクラス予測確率 (各クラスの予測確率 [クラス0の予測確率,クラス1の予測確率] を返す)
    y_pred = model.predict(x_valid)
    pred_labels = np.rint(y_pred)

    acc = accuracy_score(y_valid, pred_labels)
    return acc


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-train', '--train_file', type=str, default='./data/preprocess.csv')
    args = parser.parse_args()  # 引数解析
    print(f'Optimizing keiba_dataset...')
    #loss_list = []

    timestamp = "{0:%Y%m%d-%H%M%S}".format(datetime.datetime.now())  # タイムスタンプ
    result_dir = './result/' + timestamp + '_opt/'  # 結果を出力するディレクトリ名
    os.mkdir(result_dir)  # 結果を出力するディレクトリを作成

    best_parm = {}  # 最適なパラメータ
    study = optuna.create_study(direction='maximize')  # accuracyの方向をmaximizeに指定
    study.optimize(lgb_trial, n_trials=1000)
    best_param = {
        'metric': study.best_params['metric'],
        'lambda_l1': study.best_params['lambda_l1'],
        'lambda_l2': study.best_params['lambda_l2'],
        'num_leaves': study.best_params['num_leaves'],
        'feature_fraction': study.best_params['feature_fraction'],
        'bagging_fraction': study.best_params['bagging_fraction'],
        'bagging_freq': study.best_params['bagging_freq'],
        'min_child_samples': study.best_params['min_child_samples'],
    }
    print(best_param)

    with open(f'{result_dir}opt_parameter.json', mode='w') as f:
        json.dump(best_param, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
