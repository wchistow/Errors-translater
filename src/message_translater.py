import json
import re
from enum import Enum
from pathlib import Path

line = ''
db_path = Path(__file__).parent / 'db'


class ParserState(Enum):
    WAITING = 0
    IN_VARIABLE = 1


def _translate_simple_error(err_message: list[str]) -> str:
    global line
    line = '' if re.match(r'^File "<stdin>", line \d+, in <module>$', err_message[0]) is not None else err_message[1]

    location = _get_location(err_message[0])
    message = _get_error(err_message[1] if line == '' else err_message[2])

    if line == '':
        result = f'{location.capitalize()}:\n  {message}'
    else:
        result = f'{location.capitalize()}:\n  {line}\n{message}'
    return result


def translate_message(err_message: list[str]) -> str:
    """Возвращает русский текст ошибки."""
    global line

    err_message = err_message[1:] if err_message[0] == 'Traceback (most recent call last):' else err_message

    if len(err_message) in (2, 3):
        return _translate_simple_error(err_message)
    else:
        if 'During handling of the above exception, another exception occurred:' in err_message:
            result = ''
            error = []
            index = 0
            for _ in range(len(err_message)):
                try:
                    err_line = err_message[index]
                except IndexError:
                    result += f'{_translate_simple_error(error)}' + \
                               '\n\nВо время обработки вышеупомянутого исключения произошло следующее исключение:\n\n'
                    break

                if err_line == 'During handling of the above exception, another exception occurred:':
                    error.pop()
                    result += f'{_translate_simple_error(error)}' + \
                              '\n\nВо время обработки вышеупомянутого исключения произошло следующее исключение:\n\n'
                    index += 3
                    error = []
                else:
                    error.append(err_line)
                    index += 1

            result = '\n'.join(result.splitlines()[:-3])
            return result
        else:
            result = ''

            for err_line in err_message:
                if re.match(r'^File ".+", line \d+, in .+$', err_line) is not None or\
                       re.match(r'^File ".+", line \d+$', err_line) is not None:
                    result += f'{_get_location(err_line).capitalize()}:\n  '
                elif re.match(r'^\[Previous line repeated \d+ more times]$', err_line) is not None:
                    m = re.match(r'^\[Previous line repeated (\d+) more times]$', err_line)
                    result += f'[Предыдущая строка повторена ещё {m.groups()[0]} раз]\n'
                elif re.match(r'^[A-Z]\w+: .+$', err_line) is not None:
                    result += _get_error(err_line)
                    break
                else:  # Строка кода
                    result += f'{err_line}\n'

            if result.endswith('\n'):
                result = result[:-1]
            return result


def _get_location(location: str) -> str:
    """Возвращает русский текст места ошибки."""
    if re.match(r'^File "<stdin>", line \d+, in <module>$', location) is not None or\
           re.match(r'^File "<stdin>", line \d+$', location) is not None:
        return 'в интерпретаторе'
    else:
        file = location[6:location.rfind('"')]
        line_num = location[location.find(',') + 7: location.rfind(',')]
        return f'в файле "{file}", строке {line_num}'


def _get_error(message: str) -> str:
    """Возвращает русский текст названия и сообщения ошибки."""
    if ':' in message:
        err_type = message[:message.find(':')]
        err_message = message[message.find(':') + 2:]

        ru_type = _get_error_type(err_type).capitalize()
        ru_message = _get_message(err_type, err_message)
        return f'{ru_type}{": " if ru_message else ""}{ru_message}{"." if ru_message else ""}'
    else:  # без сообщения, например `KeyboardInterrupt`
        return _get_error_type(message).capitalize()


def _get_error_type(err_type: str) -> str:
    """Возвращает русский перевод типа ошибки."""
    with open(db_path / 'errors_types.json', encoding='utf-8') as f:
        errors_types = json.load(f)

    try:
        return errors_types[err_type]
    except KeyError:
        return 'неизвестная ошибка'


def _get_message(err_type: str, message: str) -> str:
    """Возвращает русский текст сообщения ошибки."""
    if message == 'None':
        return ''

    with open(db_path / 'errors_messages.json', encoding='utf-8') as f:
        errors_messages = json.load(f)

    try:
        messages = errors_messages[err_type]
        for k, v in messages.items():
            if re.fullmatch(re.sub(r'\$\w+\$', '.+', k), message) is not None:
                orig_message = k
                ru_message = v
                break
        else:
            return '<нет перевода>'
    except KeyError:
        return '<нет перевода>'
    else:
        if '$' in orig_message:
            state = ParserState.WAITING
            cur_name = ''
            variables = []

            for c in orig_message:
                if state == ParserState.WAITING and c == '$':  # вошли в переменную
                    state = ParserState.IN_VARIABLE
                elif state == ParserState.IN_VARIABLE and c == '$':  # вышли из переменной
                    state = ParserState.WAITING
                    variables.append(cur_name)
                    cur_name = ''
                elif state == ParserState.IN_VARIABLE:  # в переменной
                    cur_name += c

            regex = orig_message
            for variable in variables:
                regex = regex.replace(f'${variable}$', r'(.+)')

            m = re.match(regex, message)
            # Словарь вида "имя_переменной": "значение_переменной"
            for name, val in zip(variables, m.groups()):
                ru_message = ru_message.replace(f'${name}$', val)

            return ru_message
        else:
            return ru_message
