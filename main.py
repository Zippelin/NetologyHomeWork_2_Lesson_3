import time
import os
import json
from urllib import parse
import requests
import hashlib


def function_logger(path):
    def func_decorator(func):
        def logger(*args, **kwargs):
            if not os.path.exists(path):
                os.mkdir(path)
            start_exec_time = time.time()
            with open(os.path.join(path, f'{func.__name__}_{start_exec_time}.txt'), 'wt', encoding='utf-8') as log:
                log.write(f'Вызвана {func.__name__} с аргументами: {args, kwargs}\n')
                try:
                    result = func(*args, **kwargs)
                except Exception as err:
                    log.write(f'Функция завершилась с ошибкой:\n{err}\n')
                    raise err
                log.write(f'Выполнена {func.__name__}. Результат:\n{result}\n')
                log.write(f'Время выполнения {time.time() - start_exec_time}\n')
            return result
        return logger
    return func_decorator


@function_logger('logs/')
def test_func(a, b):
    return a + b


# Задание из предыдущего ДЗ
# ============================================

DB_FILE = 'db.json'
OUTPUT_FILE = 'out.txt'


# Задание 1
class WikiComposer:
    BASE_WIKI_URL = 'https://ru.wikipedia.org/wiki/'

    @function_logger('lesson2_task1_logs')
    def __init__(self, file_path):
        self.file_path = file_path
        self.result_pairs = []
        with open(DB_FILE) as f:
            self.file_data = json.load(f)
        self.__inx = -1

    def __iter__(self):
        return self

    def __next__(self):
        self.__inx += 1
        if self.__inx == len(self.file_data) - 1:
            raise StopIteration
        return self.file_data[self.__inx]

    @function_logger('lesson2_task1_logs')
    def generate_urls(self):
        with open(OUTPUT_FILE, 'wt') as f:
            for record in self:
                url = str(parse.urljoin(self.BASE_WIKI_URL, record["translations"]["rus"]["official"]))
                # Закоментил, т.к. долго запросы делаются, да и не обязательно по задаче.
                # result = requests.get(url)
                # if result.status_code != 200:
                #     url = 'нет ссылки'
                f.write(f'({record["translations"]["rus"]["official"]}, {url}),\n')


# Задание 2
@function_logger('lesson2_task2_logs')
def file_crypt(f):
    for line in f:
        yield hashlib.md5(line.encode('utf-8')).hexdigest()


def call_lesson2_task1():
    pairs_saver = WikiComposer(DB_FILE)
    pairs_saver.generate_urls()


def call_lesson2_task2():
    with open(DB_FILE, 'r') as f:
        for line in file_crypt(f):
            print(line)

# ============================================


if __name__ == '__main__':
    # Задание 1-2
    test_func(2, 1)
    # Задание 3
    call_lesson2_task1()
    call_lesson2_task2()