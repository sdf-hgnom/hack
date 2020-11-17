import random
from typing import Text
import time

import requests

N = 10

URLS = ['https://www.avito.ru/',
        'https://www.speedtest.net/',
        'https://djbook.ru/',
        'http://styxcosmetic.ru/',
        'https://www.simplifiedpython.net/',
        'https://ling47.ru/',
        ]


def test_url(what_url: Text, count: int = 10, sleep_time: int = 1) -> float:
    """
    выполнит http get запрос по  адресу если код не 200 сгенирит ошибку
    если все хорошо - подсчитает время выполнения запросов
    :param what_url: url запроса
    :param count: кол-во повторов
    :param sleep_time: задержка между повторами
    :return:
    """
    begin_time = time.monotonic()
    print(f'\nbegin test {what_url} :')
    for i in range(count):
        response = requests.get(url=what_url)
        print('.', end='')
        if response.status_code != 200:
            raise ConnectionError(f'{what_url} -> Bad response code {response.status_code} in {i} iteration ')

        time.sleep(sleep_time)

    return time.monotonic() - begin_time


def get_good_pass(password_length: int = 8):
    """Генирация хорошего пароля"""
    let = ''.join([chr(i) for i in range(97, 97 + 26)])

    let_up = let.upper()
    symbols = ''.join([chr(i) for i in range(33, 64)])
    alpha = let + let_up + symbols
    new_pass = ''

    for _ in range(password_length):
        new_pass += random.choice(alpha)
    return new_pass


def get_bad_passwords(count: int = 10):
    reading_lines = []
    with open('./common_passwords.txt', 'rt', encoding='utf-8') as file:
        for _ in range(count):
            reading_lines.append(file.readline().strip())

    def wrapper():
        for current in reading_lines:
            yield current

    return wrapper()


if __name__ == '__main__':
    print('beg')
    bad_passwords = get_bad_passwords(count=20)
    for current_password in bad_passwords:
        print(current_password)

    for url in URLS:
        try:
            time_period = test_url(what_url=url, count=100, sleep_time=5)
            print(f'\nTest end with {time_period} sec')
        except ConnectionError as ex:
            print(ex.args)
