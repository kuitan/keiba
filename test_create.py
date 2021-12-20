import pandas as pd


def create_csv():
    result_dir = './result/'  # 結果を出力するディレクトリ名

    horse_list = []
    horse_list.append([1, 1, 'カジュフェイス', '牝2', 55.0, '秋山真一', 12, 50.4, '478(0)', '[西] 森田直行', '芝右1600', '晴', '良'])
    horse_list.append([2, 2, 'セッカチケーン', '牝2', 55.0, '団野大成', 14, 158.7, '478(0)', '[東] 高柳瑞樹', '芝右1600', '晴', '良'])
    horse_list.append([2, 3, 'アルナシーム', '牝2', 55.0, '池添謙一', 6, 21.5, '478(0)', '[西] 橋口慎介', '芝右1600', '晴', '良'])
    horse_list.append([3, 4, 'セリフォス', '牝2', 55.0, 'Ｃデムー', 2, 3.6, '478(0)', '[西] 中内田充', '芝右1600', '晴', '良'])
    horse_list.append([3, 5, 'ヴィアドロローサ', '牝2', 55.0, '鮫島克駿', 11, 50.1, '478(0)', '[東] 加藤征弘', '芝右1600', '晴', '良'])
    horse_list.append([4, 6, 'オタルエバー', '牝2', 55.0, '幸英明', 7, 24.0, '478(0)', '[西] 中竹和也', '芝右1600', '晴', '良'])
    horse_list.append([4, 7, 'ダノンスコーピオン', '牝2', 55.0, '松山弘平', 4, 7.8, '478(0)', '[西] 安田隆行', '芝右1600', '晴', '良'])
    horse_list.append([5, 8, 'プルパレイ', '牝2', 55.0, 'Ｍデムー', 8, 29.0, '478(0)', '[西] 須貝尚介', '芝右1600', '晴', '良'])
    horse_list.append([5, 9, 'ドウデュース', '牝2', 55.0, '武豊', 3, 6.1, '478(0)', '[西] 友道康夫', '芝右1600', '晴', '良'])
    horse_list.append([6, 10, 'スプリットザシー', '牝2', 54.0, '和田竜二', 10, 40.3, '478(0)', '[西] 西村真幸', '芝右1600', '晴', '良'])
    horse_list.append([6, 11, 'ドーブネ', '牝2', 55.0, '吉田隼人', 5, 12.5, '478(0)', '[西] 武幸四郎', '芝右1600', '晴', '良'])
    horse_list.append([7, 12, 'トウシンマカオ', '牝2', 55.0, '戸崎圭太', 9, 38.4, '478(0)', '[東] 高柳瑞樹', '芝右1600', '晴', '良'])
    horse_list.append([7, 13, 'ジオグリフ', '牝2', 55.0, 'ルメール', 1, 3.2, '478(0)', '[東] 木村哲也', '芝右1600', '晴', '良'])
    horse_list.append([8, 14, 'トゥードジボン', '牝2', 55.0, '藤岡佑介', 13, 104.7, '478(0)', '[西] 四位洋文', '芝右1600', '晴', '良'])
    horse_list.append([8, 15, 'シンリミテス', '牝2', 55.0, '国分優作', 15, 221.7, '478(0)', '[西] 大根田裕', '芝右1600', '晴', '良'])
    # horse_list.append([8, 18, 'パーソナルハイ', '牝2', 54.0, '藤岡康太', 7, 41.7, '462(-8)', '[西] 矢作芳人', '芝右1600', '晴', '良'])
    # horse_list.append([1, 2, 'ナムラリコリス', '牝2', 54.0, '泉谷楓真', 13, 111.3, '476(+12)', '[西] 大橋勇樹', '芝右1600', '晴', '良'])
    # horse_list.append([2, 3, 'ヒノクニ', '牝2', 54.0, '長岡禎仁', 17, 261.2, '446(+8)', '[東] 深山雅史', '芝右1600', '晴', '良'])

    columns = ['枠番', '馬番', '馬名', '性齢', '斤量', '騎手', '人気', '単勝', '馬体重', '調教師', 'レース名', '天候', '芝状態']
    df = pd.DataFrame(horse_list, columns=columns)

    print(df)

    # CSVファイルとして出力
    df.to_csv(f'{result_dir}test.csv', index=False)


if __name__ == '__main__':
    create_csv()