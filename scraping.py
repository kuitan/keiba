import requests
from bs4 import BeautifulSoup
import re
import time
import pandas as pd
from datetime import date
from utils import date_range


def get_data(url, proxies):
    result_dir = './result/'  # 結果を出力するディレクトリ名

    for d in date_range(date(2011, 1, 1), date(2022, 3, 23)):
        # dateを使った処理
        d = d.strftime("%Y%m%d")

        res = requests.get(f'{url}/race/list/{d}/', proxies=proxies)
        time.sleep(1)

        # レースリストを取得
        soup = BeautifulSoup(res.content, "html.parser")
        soup = soup.select_one('div.race_kaisai_info')

        if soup is not None:
            print(f'{url}/race/list/{d}/')

            race_list = soup.find_all('a', href=re.compile('/race/[0-90-9]+'))

            # 各レース結果からデータを抽出
            for i, race in enumerate(race_list):
                race_url = race.attrs['href']
                res = requests.get(f'{url}{race_url}', proxies=proxies)
                soup = BeautifulSoup(res.content, "html.parser")

                df = pd.read_html(res.content, match='馬名')[0]  # Tableを抽出

                # horse_idを取得
                race_table = soup.select_one('table[class="race_table_01 nk_tb_common"]')
                horse_list = race_table.find_all('a', href=re.compile('/horse/[0-90-9]+'))
                horse_id_list = []
                [horse_id_list.append(horse_url.attrs['href'].split('/')[2]) for horse_url in horse_list]

                # jockey_idを取得
                jockey_list = race_table.find_all('a', href=re.compile('/jockey/[0-90-9]+'))
                jockey_id_list = []
                [jockey_id_list.append(jockey_url.attrs['href'].split('/')[2]) for jockey_url in jockey_list]

                # trainer_idを取得
                trainer_list = race_table.find_all('a', href=re.compile('/trainer/[0-90-9]+'))
                trainer_id_list = []
                [trainer_id_list.append(trainer_url.attrs['href'].split('/')[2]) for trainer_url in trainer_list]

                soup = soup.select_one('dl.racedata')
                race_title = soup.select_one('h1')
                race_title = race_title.contents[0]
                df['レース種類'] = race_title

                race_cond = soup.select_one('span')
                race_cond = race_cond.contents[0].split('/')
                df['レース名'] = race_cond[0]

                race_cond_whether = race_cond[1].split(':')
                df['天候'] = race_cond_whether[1]

                race_cond_status = race_cond[2].split(':')
                df['芝状態'] = race_cond_status[1]

                race_cond_time = race_cond[3].split()
                df['発走'] = race_cond_time[2]

                df.insert(4, 'horse_id', horse_id_list)
                df.insert(8, 'jockey_id', jockey_id_list)
                df.insert(15, 'trainer_id', trainer_id_list)

                # 日付を追加
                df['date'] = d

                # 払い戻しを取得
                df_pay = pd.read_html(res.content, match='三連複')[0]  # Tableを抽出
                df['三連複'] = df_pay.iat[2, 1]
                df['払い戻し'] = df_pay.iat[2, 2]

                print(df)
                # print(df_pay)

                if i == 0:
                    df1 = df
                else:
                    df2 = df
                    df1 = pd.concat([df1, df2])
                    # print(df1)

                time.sleep(1)

            # print(df1)
            # CSVファイルとして出力
            df1.to_csv(f'{result_dir}{d}.csv', index=False)

        else:
            print('pass')


if __name__ == '__main__':
    url = 'https://db.netkeiba.com'
    proxies = {
        "http": "http://proxy.nagaokaut.ac.jp:8080",
        "https": "http://proxy.nagaokaut.ac.jp:8080"
    }
    get_data(url, proxies)