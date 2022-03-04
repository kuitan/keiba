import requests
from bs4 import BeautifulSoup
import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def get_test_data(url):
    result_dir = './result/'  # 結果を出力するディレクトリ名

    # ブラウザを起動
    options = Options()
    options.add_argument('--headless')
    chrome_service = service.Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=chrome_service, options=options)

    driver.get(url)
    time.sleep(1)

    pd.set_option('display.max_columns', 100)

    # htmlを取得
    source_code = driver.page_source

    print(url)

    df = pd.read_html(source_code, match='馬名')[0]  # Tableを抽出
    df.columns = df.columns.droplevel(0)  # headerのMultiIndexを解除

    # 騎手のリストを取得
    soup = BeautifulSoup(source_code, "html.parser")
    race_table = soup.select_one('div.RaceTableArea')
    jockey_url_list = race_table.find_all('a', href=re.compile('/jockey/[0-90-9]+'))

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
                            '馬体重(増減)': 'horse_weight', '予想オッズ': 'win', '人気': 'popular'})
    df = df.reindex(columns=['frame_num', 'horse_num', 'horse_name', 'sex_age', 'weight_to_carry', 'jockey', 'popular',
                             'win', 'horse_weight', 'trainer'])

    df['jockey'] = jockey_list
    df['trainer'] = trainer_list
    print(df.head())

    # ブラウザを閉じる
    driver.quit()

    # CSVファイルとして出力
    df.to_csv(f'{result_dir}test.csv', index=False)


if __name__ == '__main__':
    url = 'https://race.netkeiba.com/race/shutuba.html?race_id=202209010711&rf=race_submenu'
    get_test_data(url)