import requests
from bs4 import BeautifulSoup
import re
import time
import pandas as pd
from datetime import date


def get_data(url, proxies):
    result_dir = './result/'  # 結果を出力するディレクトリ名

    res = requests.get(f'{url}/race/result.html?race_id=202109060411&rf=race_list', proxies=proxies)
    time.sleep(1)

    soup = BeautifulSoup(res.content, "html.parser")
    soup = soup.select_one('div.ResultTableWrap')
    print(soup)

    # df = pd.read_html(res.content, match='性齢')  # Tableを抽出
    # print(df)

    # CSVファイルとして出力
    # df.to_csv(f'{result_dir}{d}.csv', index=False)


if __name__ == '__main__':
    url = 'https://db.netkeiba.com'
    proxies = {
        "http": "http://proxy.nagaokaut.ac.jp:8080",
        "https": "http://proxy.nagaokaut.ac.jp:8080"
    }
    get_data(url, proxies)