from django.core.management.base import BaseCommand
#from logs.models import Record
import requests
import re

"""
План
IP + Дата + Тип запроса + Код ответа + Размер ответа + URL  
"""


class Command(BaseCommand):
    """Принимает ссылку на сайт с логами"""

    help = 'Run to parse logs from your link to database'

    # def add_arguments(self, parser):
    #    parser.add_argument('link', type=str)

    def handle(self, *args, **options):
        # link = options.get('link')
        # log_file = requests.get(link).text # [1:233]  # get-запрос
        with open('log.txt') as f:

            WSP, QUOTED_STRING, DATE, RAW, NO_DATA = range(5)  # ENUM
            rules = [
                ('\s+', WSP),
                ('-|"-"', NO_DATA),
                ('"([^"]+)"', QUOTED_STRING),
                ('\[([^\]]+)\]', DATE),
                ('([^\s]+)', RAW),
            ]
            log_file = f.read()
            # regexp = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
            prepared = [(re.compile(regexp), token_type) for regexp, token_type in rules]
            # data = '((\d{2}|\d{4})/(\d{2}|\w{3})/(\d{2}|\d{4})(?:\:|\s+))'
            # ips_list = re.findall(regexp, log_file)
            ll = len(log_file)
            i = 0
            while i < ll:
                #print(i)
                for pattern, token_type in prepared:
                    match = pattern.match(log_file, i)
                    #match = re.match(regexp, log_file, i)
                    # print(match.group(0))
                    if match is None:
                        continue
                    i = match.end()
                    print(match.group(0), token_type)
                    break
                #print(match)


Command.handle(Command)
