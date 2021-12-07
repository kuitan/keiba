import requests


def get_data(url):
    response = requests.get(url)
    response.text[:500]


if __name__ == '__main__':
    url = 'https://www.netkeiba.com/'
    get_data(url)