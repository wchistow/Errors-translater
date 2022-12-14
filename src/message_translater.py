import json
import re

line = ''


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
                if re.match(r'^File ".+", line \d+, in .+$', err_line) is not None:
                    result += f'{_get_location(err_line).capitalize()}:\n  '
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
    if re.match(r'^File "<stdin>", line \d+, in <module>$', location):
        return 'в интерпретаторе'
    else:
        file = location[6:location.rfind('"')]
        line_num = location[location.find(',') + 7: location.rfind(',')]
        return f'в файле "{file}", строке {line_num}'


def _get_error(message: str) -> str:
    """Возвращает русский текст названия и сообщения ошибки."""
    err_type = message[:message.find(':')]
    err_message = message[message.find(':') + 2:]

    ru_type = _get_error_type(err_type).capitalize()
    ru_message = _get_message(err_type, err_message)
    return f'{ru_type}{": " if ru_message else ""}{ru_message}{"." if ru_message else ""}'


def _get_error_type(err_type: str) -> str:
    """Возвращает русский перевод типа ошибки."""
    errors_types = json.load(open('db/errors_types.json', encoding='utf-8'))

    try:
        return errors_types[err_type]
    except KeyError:
        return 'неизвестная ошибка'


def _get_message(err_type: str, message: str) -> str:
    """Возвращает русский текст сообщения ошибки."""
    errors_messages = json.load(open('db/errors_messages.json', encoding='utf-8'))

    if message == 'None':
        return ''

    try:
        messages = errors_messages[err_type]
        if isinstance(messages, dict):
            try:
                return messages[message]
            except KeyError:
                return 'неизвестная ошибка'
        else:
            return messages
    except KeyError:
        match err_type:
            case 'NameError':
                if re.match(r"^name '\w+' is not defined[.| ]$", message) is not None:
                    name = message[6: message.rfind("'")]
                    return f"имя '{name}' не определено"
                elif re.match(r"^name '\w+' is not defined. Did you mean: '\w+'\?$", message) is not None:
                    name = ''
                    in_name = False
                    for s in message:
                        if s == "'" and name == '':
                            in_name = True
                        elif s == "'" and name != '':
                            in_name = False
                        elif in_name:
                            name += s
                    mean_name = ''
                    in_mean_name = False
                    for s in message[message.find('.'):]:
                        if s == "'" and mean_name == '':
                            in_mean_name = True
                        elif s == "'" and mean_name != '':
                            in_mean_name = False
                        elif in_mean_name:
                            mean_name += s
                    return f"имя '{name}' не определено. Может быть вы имели ввиду '{mean_name}'?"
            case 'TypeError':
                if re.match(r"unsupported operand type\(s\) for [+\-*/|&^]: '\w+' and '\w+'", message) is not None:
                    operator = message[32: 33]
                    operand1 = message[message.find("'") + 1: message.find("'", message.find("'") + 1)]
                    operand2 = message[47: message.rfind("'")]
                    return f"неподдерживаемый оператор {operator} для типов '{operand1}' и '{operand2}'"
            case 'FileNotFoundError':
                return f'{message[38:-1]}'
        return 'неизвестная ошибка'
