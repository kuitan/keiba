import requests
from bs4 import BeautifulSoup
import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import numpy as np


def get_test_data(url):
    result_dir = './result/'  # 結果を出力するディレクトリ名

    # ブラウザを起動
    options = Options()
    options.add_argument('--headless')
    chrome_service = service.Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=chrome_service, options=options)

    # 検索
    driver.get(url)
    time.sleep(1)

    pd.set_option('display.max_columns', 100)

    # htmlを取得
    source_code = driver.page_source

    print(url)

    df = pd.read_html(source_code, match='馬名')[0]  # Tableを抽出
    df.columns = df.columns.droplevel(0)  # headerのMultiIndexを解除

    # レース情報を取得
    soup = BeautifulSoup(source_code, "html.parser")
    race_origin = soup.select_one('div.RaceData01')
    race_name = race_origin.select_one('span').contents[0].replace(' ', '')
    race_name_other = re.split('[()]', race_origin.contents[3].split('/')[0].replace(' ', ''))[1][0]
    race_name = race_name[0] + race_name_other + race_name[1:]  # レース名
    try:
        race_weather = race_origin.contents[3].split('/')[1].split(':')[1]  # 天候
        race_cond = race_origin.select_one('span[class="Item03"]').contents[0].split(':')[1]  # レースの状態
    except IndexError:
        race_weather = np.nan
        race_cond = np.nan
    race_type = re.split('[()]', soup.title.contents[0])[1]  # レースの種類

    # 騎手のリストを取得
    soup = BeautifulSoup(source_code, "html.parser")
    race_table = soup.select_one('div.RaceTableArea')
    jockey_url_list = race_table.find_all('a', href=re.compile('/jockey/[0-90-9]+'))

    # horse_idを取得
    horse_list = race_table.find_all('a', href=re.compile('/horse/[0-90-9]+'))
    horse_id_list = []
    [horse_id_list.append(horse_url.attrs['href'].split('/')[4]) for horse_url in horse_list]
    # jockey_idを取得
    jockey_list = race_table.find_all('a', href=re.compile('/jockey/[0-90-9]+'))
    jockey_id_list = []
    [jockey_id_list.append(jockey_url.attrs['href'].split('/')[4]) for jockey_url in jockey_list]
    # trainer_idを取得
    trainer_list = race_table.find_all('a', href=re.compile('/trainer/[0-90-9]+'))
    trainer_id_list = []
    [trainer_id_list.append(trainer_url.attrs['href'].split('/')[4]) for trainer_url in trainer_list]

    jockey_list = []
    for jockey in jockey_url_list:
        # 各騎手名を取得
        jockey_url = jockey.attrs['href']
        res = requests.get(jockey_url)
        time.sleep(1)
        soup = BeautifulSoup(res.content, "html.parser")
        title = soup.find('title').text
        jockey_list.append(title.split(' ')[0].replace('．', '')[:4])

    # 調教師のリストを取得
    trainer_url_list = race_table.find_all('a', href=re.compile('/trainer/[0-90-9]+'))

    trainer_list = []
    for trainer, trainer_origin in zip(trainer_url_list, df['厩舎']):
        # 各調教師名を取得
        trainer_url = trainer.attrs['href']
        res = requests.get(trainer_url)
        time.sleep(1)
        soup = BeautifulSoup(res.content, "html.parser")
        title = soup.find('title').text
        trainer_name = title.split(' ')[0][:4]
        if trainer_origin[:2] == '栗東':
            trainer_type = '[西] '
        elif trainer_origin[:2] == '美浦':
            trainer_type = '[東] '
        else:
            trainer_type = '[地] '
        trainer_list.append(trainer_type + trainer_name)

    # 不要な属性を削除
    del df['印']
    del df['登録']
    del df['メモ']

    # ヘッダーを変更，並び替え
    df = df.rename(columns={'枠': 'frame_num', '馬番': 'horse_num', '馬名': 'horse_name', '性齢': 'sex_age',
                            '斤量': 'weight_to_carry', '騎手': 'jockey', '厩舎': 'trainer',
                            '馬体重(増減)': 'horse_weight', 'オッズ 更新': 'win', '予想オッズ': 'win', '人気': 'popular'})

    df = df.reindex(columns=['frame_num', 'horse_num', 'horse_name', 'sex_age', 'weight_to_carry', 'jockey', 'popular',
                             'win', 'horse_weight', 'trainer'])

    # 値の置き換え
    df['jockey'] = jockey_list
    df['trainer'] = trainer_list

    # 馬体重を使わない場合
    if pd.isnull(df['horse_weight'][0]):
        df['horse_weight'] = '502(0)'

    # レース名，天候，レース状態を追加
    df['race_name'] = race_name

    df['weather'] = race_weather
    # 天候を使わない場合
    if pd.isnull(df['weather'][0]):
        df['weather'] = '晴'

    df['race_cond'] = race_cond
    # 馬場状態を使わない場合
    if pd.isnull(df['race_cond'][0]):
        df['race_cond'] = '良'

    df['race_type'] = race_type

    df.insert(3, 'horse_id', horse_id_list)
    df.insert(7, 'jockey_id', jockey_id_list)
    df.insert(12, 'trainer_id', trainer_id_list)

    print(df.head())

    # ブラウザを閉じる
    driver.quit()

    # CSVファイルとして出力
    df.to_csv(f'{result_dir}test.csv', index=False)


if __name__ == '__main__':
    url = 'https://race.netkeiba.com/race/shutuba.html?race_id=202206030111&rf=race_submenu'
    get_test_data(url)