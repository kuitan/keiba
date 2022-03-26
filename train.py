import lightgbm as lgb
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, log_loss, roc_auc_score, roc_curve
import pandas as pd
from utils import display, plot_feature_importance
import matplotlib.pyplot as plt
import numpy as np
from torch.utils.data import DataLoader, TensorDataset
from neural_net import Ann
import torch
import torch.nn as nn
from torch.optim import SGD
from torch.autograd import Variable
from utils import get_device
import itertools
from sklearn.datasets import load_wine


def train(param):
    device = get_device()  # デバイスを取得

    train_file = param['train_file']
    test_file = param['test_file']
    model_param = param['model']
    load_dir = param['load']
    result_dir = param['result_dir']

    # keibaデータセットの読み込み
    df = pd.read_csv(f'{train_file}')
    df_test = pd.read_csv(f'{test_file}')

    # ワインデータセットの読み込み
    # wine = load_wine()
    # wine_df = pd.DataFrame(wine.data, columns=wine.feature_names)
    # wine_class = pd.DataFrame(wine.target, columns=['class'])

    # データの確認
    print(df.shape)  # データサイズの確認(データ数, 特徴量数)
    display(df)  # df.head()に同じ(文中に入れるときはdisplay()を使う)

    # 説明変数,目的変数
    x = df.drop('target', axis=1).values  # 説明変数(target以外の特徴量)
    y = df['target'].values  # 目的変数(target)
    if model_param == 'gbm':
        t = df_test
    else:
        t = df_test.values

    # wine_cat = pd.concat([wine_df, wine_class], axis=1)
    # wine_cat.drop(wine_cat[wine_cat['class'] == 2].index, inplace=True)
    # wine_data = wine_cat.values[:, :13]
    # wine_target = wine_cat.values[:, 13]

    # トレーニングデータ,テストデータの分割
    x_train, x_valid, y_train, y_valid = train_test_split(x, y, test_size=0.20)
    # x_train, x_valid, y_train, y_valid = train_test_split(wine_data, wine_target, test_size=0.25)

    # クラスの比率
    n_target0, n_target1 = len(df[df['target'] == 0]), len(df[df['target'] == 1])
    n_all = n_target0 + n_target1
    print('target0 の割合 :', n_target0/n_all)  # target0(4位以下)の割合
    print('target1 の割合 :', n_target1/n_all)  # target1(3位以内)の割合

    # 学習に使用するデータを設定
    if model_param == 'gbm':
        lgb_train = lgb.Dataset(x_train, y_train)
        lgb_eval = lgb.Dataset(x_valid, y_valid, reference=lgb_train)
    else:
        x_train = torch.FloatTensor(x_train)
        y_train = torch.LongTensor(y_train)
        x_valid = torch.FloatTensor(x_valid)
        y_valid = torch.LongTensor(y_valid)
        t = torch.FloatTensor(t)
        train_tensor = TensorDataset(x_train, y_train)
        valid_tensor = TensorDataset(x_valid, y_valid)

        train_dataloader = DataLoader(train_tensor, batch_size=4096, shuffle=True)  # 2048
        valid_dataloader = DataLoader(valid_tensor, batch_size=4096, shuffle=False)  # 2048

        model = Ann(input_dim=23).to(device)  # 26
        criterion = nn.CrossEntropyLoss()
        optimizer = SGD(model.parameters(), lr=0.01)

    # ハイパーパラメータ
    if model_param == 'gbm':
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

        # モデルの学習(LightGBM)
        model = lgb.train(params, train_set=lgb_train, valid_sets=lgb_eval)
        model.save_model(f'{result_dir}model.txt', num_iteration=model.best_iteration)

    else:
        if load_dir is not None:  # ロードオプションが指定されていたらロード
            model.load_state_dict(torch.load(f'{load_dir}lstm.nn', map_location=device))  # モデルを読み込み
        else:
            # モデルの学習(ANN)
            epoch_num = 100
            loss_list = []
            loss_test_list = []
            for epoch in range(epoch_num):
                total_loss = 0
                for train_x, train_y in train_dataloader:
                    train_x, train_y = train_x.to(device), train_y.to(device)
                    optimizer.zero_grad()
                    output = model(train_x)
                    loss = criterion(output, train_y)
                    loss.backward()
                    optimizer.step()
                    total_loss += loss.item()

                # テスト
                total_test_loss = 0
                with torch.no_grad():
                    for valid_x, valid_y in valid_dataloader:
                        valid_x, valid_y = Variable(valid_x).to(device), Variable(valid_y).to(device)
                        output = model(valid_x)
                        loss = criterion(output, valid_y)
                        total_test_loss += loss.item()

                print('epoch:', epoch + 1, ', train_loss:', total_loss, ', valid_loss: ', total_test_loss)
                loss_list.append(total_loss)
                loss_test_list.append(total_test_loss)
            torch.save(model.state_dict(), f'{result_dir}lstm.nn')

            # lossのグラフの表示
            plt.figure()
            plt.plot(np.arange(epoch_num), loss_list)
            plt.xlabel('epoch')
            plt.ylabel('loss')
            plt.savefig(f'{result_dir}loss.png')
            plt.close()

            plt.figure()
            plt.plot(np.arange(epoch_num), loss_test_list)
            plt.xlabel('epoch')
            plt.ylabel('loss')
            plt.savefig(f'{result_dir}valid_loss.png')
            plt.close()

    if model_param == 'gbm':
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
        idx = np.arange(1, len(df_pred_prob) + 1)
        df_pred_prob['horse_num'] = idx  # 馬番を追加
        df_s = df_pred_prob.sort_values('target1_prob', ascending=False)
        del df_s['target0_prob']
        print(df_s)

        # 買い目の馬を返す
        # 上位3つの三連複を買う場合
        bet_top_list = df_s[:3]['horse_num'].values.tolist()
        print(bet_top_list)

        # 上位5つの三連複をボックスで買う場合
        triple_list = df_s[:5]['horse_num'].values.tolist()
        bet_box_list = [list(bet) for bet in itertools.combinations(triple_list, 3)]
        print(bet_box_list)

        # 上位5つの三連複をフォーメーションで買う場合
        triple_list = df_s[:3]['horse_num'].values.tolist()
        bet_list_head = [list(bet) for bet in itertools.combinations(triple_list, 2)]
        triple_list = df_s[3:5]['horse_num'].values.tolist()
        bet_form_list = []
        for bet_list in bet_list_head:
            bet_list1 = []
            bet_list2 = []
            for bet in bet_list:
                bet_list1.append(bet)
                bet_list2.append(bet)
            bet_list1.append(triple_list[0])
            bet_list2.append(triple_list[1])
            bet_form_list.append(bet_list1)
            bet_form_list.append(bet_list2)
        print(bet_form_list)

        return bet_top_list, bet_box_list, bet_form_list
    else:
        # モデル評価
        x_valid, y_valid = x_valid.to(device), y_valid.to(device)
        result = torch.max(model(x_valid).detach(), 1)[1]
        y_valid = y_valid.to('cpu').detach().numpy().copy()
        result = result.to('cpu').detach().numpy().copy()
        acc = sum(y_valid == np.array(result, dtype='float64')) / len(y_valid)
        print('Acc :', acc)

        # テストデータの予測値の表示
        t = t.to(device)

        # テストデータのクラス予測確率
        t_pred = model(t, test=True).detach()
        t_pred = t_pred.to('cpu').detach().numpy().copy()
        t_pred_0 = t_pred.T[0]
        t_pred_1 = t_pred.T[1]

        df_pred_prob = pd.DataFrame({'target0_prob': t_pred_0, 'target1_prob': t_pred_1})
        idx = np.arange(1, len(df_pred_prob) + 1)
        df_pred_prob['horse_num'] = idx  # 馬番を追加
        df_s = df_pred_prob.sort_values('target1_prob', ascending=False)
        print(df_s)