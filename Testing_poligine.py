import re


WSP, QUOTED_STRING, DATE, RAW, NO_DATA = range(5) # ENUM

RULES = [
    ('\s+', WSP), # Пробелы
    ('-|"-"', NO_DATA), # Элемент отсутствует
    ('"([^"]+)"', QUOTED_STRING), # Строка в скобках
    ('\[([^\]]+)\]', DATE), # Дата
    ('([^\s]+)', RAW), # Беспрерывная строка
    ]


def lexer(rules):
    # предварительно компилируем регулярные выражения для ускорения работы
    prepared = [(re.compile(regexp), token_type) for regexp, token_type in rules]
    print(prepared)

    def lex(line):
        print('hello')
        ll = len(line) # длина строки лога - чтобы знать, когда остановиться
        i = 0          # текущая позиция анализатора
        while i < ll:
            for pattern, token_type in prepared:  # пробуем регулярные выражения по очереди
                match = pattern.match(line, i)    # проверяем соответствует ли регулярное выражение строке с позиции i
                if match is None:                 # если нет - пробуем следующую регулярку
                    continue
                i = match.end()                   # передвигаем позицию анализатора до индекса, соответствующего концу совпадения
                yield (match, token_type)         # возвращаем найденный токен
                break                             # начинаем анализировать остаток строки с новым значением сдвига i
            # по хорошему, в этом месте нужно кидать ошибку SyntaxError(line, i) в случае, если ни один из шаблонов не совпал


def reader(filename):
    with open(filename) as f:
        log = f.read()
        print(log)


if __name__ == '__main__':
    lexer(RULES)
    # reader('log.txt')
