import datetime

from django.core.management.base import BaseCommand
from logs.models import Record
import requests
import re

"""
План
IP + Дата + Тип запроса + Код ответа + Размер ответа + URL  
"""


def create_record(ip, date, http_method, url, answer_code, answer_size):
    """Создает запись в базу дынных"""
    Record.objects.create(ip=ip,
                          date=date,
                          http_method=http_method,
                          url=url,
                          answer_code=answer_code,
                          answer_size=answer_size
                          )


class Command(BaseCommand):
    """Принимает ссылку на сайт с логами"""

    help = 'Run to parse logs from your link to database'

    def add_arguments(self, parser):
        parser.add_argument('link', type=str)

    def handle(self, *args, **options):
        link = options.get('link')
        log_file = requests.get(link).text # [1:233]  # get-запрос
        # with open('logs/management/commands/log.txt') as f:
        # log_file = open('logs/management/commands/log.txt', 'r')
        # log_file = log_file.read()
        WSP, QUOTED_STRING, DATE, RAW, NO_DATA, DASH, IP = range(7)  # ENUM
        rules = [
            ('\s+', WSP),                   # Пробелы
            ('""|"-"', NO_DATA),            # Нет элемента
            ('-', DASH),                    # Тире
            ('"([^"]+)"', QUOTED_STRING),   # Что-то в кавычках
            ('\[([^\]]+)\]', DATE),         # Дата в квадратных скобках
            (r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', IP),    # 6 IP
            ('([^\s]+)', RAW),              # Чистые данные (нам нужны здесь только код и размер ответа)
        ]
        prepared = [(re.compile(regexp), token_type) for regexp, token_type in rules]
        ll = len(log_file)
        i = 0
        answer = []
        while i < ll:
            for pattern, token_type in prepared:    # Подставляем каждое регулярное выражения
                match = pattern.match(log_file, i)
                if match is None:
                    continue
                i = match.end()
                if token_type != WSP and token_type != DASH:     # Убираем отступы и тире
                    # print(match.group(0), token_type)
                    if token_type == IP and answer:      # Лог всегда начинается с IP
                        print(answer)
                        create_record(answer[0], answer[1], answer[2], answer[5], answer[3], answer[4])
                        answer = []
                    if token_type == QUOTED_STRING:     # Ищем тип запроса
                        match = match.group(1)
                        value = re.match(r"[A-Z]{3,10}\s", match)
                        if value:
                            answer.append(value.group(0))
                        else:   # Если запроса нет,значит это информация о браузере в кавычках
                            answer.append(match)
                        break
                    if token_type == NO_DATA:   # Проверяем если элемент отсутствует
                        match = None
                        answer.append(match)
                        break
                    if token_type == RAW:   # Нам нужны только целые числа для кода ответа и размера ответа
                        if match.group(0).isdigit():
                            answer.append(match.group(0))
                        break
                    if token_type == DATE:  # Парсим дату
                        match = re.match(r'([^\s]+)', match.group(1))
                        match = datetime.datetime.strptime(match.group(0), "%d/%b/%Y:%H:%M:%S").timetuple()
                        date = str(match.tm_year) + '-' + str(match.tm_mon) + '-' + str(match.tm_mday)
                        answer.append(date)
                        break
                    answer.append(match.group(0))
                break
        print(answer)
        create_record(answer[0], answer[1], answer[2], answer[5], answer[3], answer[4])   # Не теряем последний элемент
