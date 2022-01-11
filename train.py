import lightgbm as lgb
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, log_loss, roc_auc_score, roc_curve
import pandas as pd
from utils import display, plot_feature_importance
import matplotlib.pyplot as plt
import numpy as np


def train(param, result_dir):
    train_file = param['train_file']
    test_file = param['test_file']

    # keibaデータセットの読み込み
    df = pd.read_csv(f'{train_file}')
    df_test = pd.read_csv(f'{test_file}')

    # データの確認
    print(df.shape)  # データサイズの確認(データ数, 特徴量数)
    display(df)  # df.head()に同じ(文中に入れるときはdisplay()を使う)

    # 説明変数,目的変数
    x = df.drop('target', axis=1).values  # 説明変数(target以外の特徴量)
    y = df['target'].values  # 目的変数(target)
    t = df_test

    # トレーニングデータ,テストデータの分割
    x_train, x_valid, y_train, y_valid = train_test_split(x, y, test_size=0.20, random_state=0)

    # クラスの比率
    n_target0, n_target1 = len(df[df['target'] == 0]), len(df[df['target'] == 1])
    n_all = n_target0 + n_target1
    print('target0 の割合 :', n_target0/n_all)  # target0(3位以下)の割合
    print('target1 の割合 :', n_target1/n_all)  # target1(2位以内)の割合

    # 学習に使用するデータを設定
    lgb_train = lgb.Dataset(x_train, y_train)
    lgb_eval = lgb.Dataset(x_valid, y_valid, reference=lgb_train)

    # ハイパーパラメータ
    params = {
        'task': 'train',
        'boosting_type': 'gbdt',
        'objective': 'binary',  # 目的: 2クラス分類
        'metric': {'binary_error'},  # 評価指標: 誤り率(= 1-正答率)
        # 'num_leaves': 64,
        # 'min_data_in_leaf': 20,
        # 'max_depth': 7,
        # 'num_iteration': 1000,  # epoch
        # 'verbose': 0,
        # 'bagging_fraction': 0.7005946250957218,
        # 'bagging_freq': 2,
        # 'feature_fraction': 0.9536941283543565,
        # 'lambda_l1': 0.0007791579526795777,
        # 'lambda_l2': 0.00039109643894750883,
        # 'min_child_samples': 59,
        # 'num_leaves': 30
    }

    # モデルの学習
    model = lgb.train(params, train_set=lgb_train, valid_sets=lgb_eval)
    model.save_model(f'{result_dir}model.txt', num_iteration=model.best_iteration)

    # 特徴量重要度の算出 (データフレームで取得)
    cols = list(df.drop('target', axis=1).columns)  # 特徴量名のリスト(目的変数target以外)
    f_importance = np.array(model.feature_importance())  # 特徴量重要度の算出
    f_importance = f_importance / np.sum(f_importance)  # 正規化(必要ない場合はコメントアウト)
    df_importance = pd.DataFrame({'feature': cols, 'importance': f_importance})
    df_importance = df_importance.sort_values('importance', ascending=False)  # 降順ソート
    display(df_importance)

    # 特徴量重要度の可視化
    plot_feature_importance(df_importance, result_dir)

    # 評価データのクラス予測確率 (各クラスの予測確率 [クラス0の予測確率,クラス1の予測確率] を返す)
    y_pred_prob = model.predict(x_valid)
    # 評価データの予測クラス(予測クラス(0 or 1)を返す)
    y_pred = np.where(y_pred_prob < 0.5, 0, 1)  # 0.5より小さい場合0, そうでない場合1

    # テストデータのクラス予測確率
    t_pred_prob = model.predict(t)
    # テストデータの予測クラス
    t_pred = np.where(t_pred_prob < 0.5, 0, 1)  # 0.5より小さい場合0, そうでない場合1

    # 真値と予測値の表示
    df_pred = pd.DataFrame({'target': y_valid, 'pred': y_pred})
    display(df_pred)

    # 真値と予測確率の表示
    df_pred_prob = pd.DataFrame({'target': y_valid, 'target0_prob': 1 - y_pred_prob, 'target1_prob': y_pred_prob})
    display(df_pred_prob)

    # モデル評価
    acc = accuracy_score(y_valid, y_pred)
    print('Acc :', acc)

    # LogLoss
    loss = log_loss(y_valid, y_pred_prob)  # 引数 : log_loss(正解クラス, [クラス0の予測確率, クラス1の予測確率])
    print('Log Loss :', loss)

    # AUC
    auc = roc_auc_score(y_valid, y_pred_prob)  # 引数 : roc_auc_score(正解クラス, クラス1の予測確率)
    print('AUC :', auc)

    # ROC曲線: 評価指標AUCを算出する際に用いる曲線
    fpr, tpr, thresholds = roc_curve(y_valid, y_pred_prob)
    auc = metrics.auc(fpr, tpr)
    plt.figure()
    plt.plot(fpr, tpr, label='ROC curve (area = %.2f)' % auc)
    plt.legend()
    plt.xlabel('FPR: False positive rate')
    plt.ylabel('TPR: True positive rate')
    plt.grid()
    plt.savefig(f'{result_dir}roc_curve.png')
    plt.close()

    # テストデータの予測値の表示
    # df_pred = pd.DataFrame({'pred': t_pred})
    df_pred_prob = pd.DataFrame({'target0_prob': 1 - t_pred_prob, 'target1_prob': t_pred_prob})
    # print(df_pred)
    print(df_pred_prob)

    # 買い目の馬を表示
    idx = np.arange(1, len(df_pred_prob)+1)
    df_pred_prob['horse_num'] = idx  # 馬番を追加
    df_s = df_pred_prob.sort_values('target1_prob', ascending=False)
    del df_s['target0_prob']
    print(df_s)