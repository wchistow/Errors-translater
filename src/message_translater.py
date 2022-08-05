import re


def translate_message(err_message: list[str]) -> str:
    """Возвращает русский текст ошибки."""
    err_message = err_message[1:] if err_message[0] == 'Traceback (most recent call last):' else err_message
    result = f'{_get_location(err_message[0]).capitalize()}:\n  {err_message[1]}\n{_get_error(err_message[2])}'
    return result


def _get_location(location: str) -> str:
    """Возвращает русский текст места ошибки."""
    file = location[6:location.rfind('"')]
    line = location[location.find(',') + 7: location.rfind(',')]
    return f'в файле "{file}", строке {line}'


def _get_error(message: str) -> str:
    """Возвращает русский текст названия и сообщения ошибки."""
    err_type = message[:message.find(':')]
    err_message = message[message.find(':') + 2:]
    return f'{_get_error_type(err_type).capitalize()}: {_get_message(err_type, err_message)}.'


def _get_error_type(err_type: str) -> str:
    """Возвращает русский перевод типа ошибки."""
    match err_type:
        case 'NameError':
            return 'ошибка имени'
        case 'ValueError':
            return 'ошибка значения'
        case 'TypeError':
            return 'ошибка типа'
        case 'SyntaxError':
            return 'ошибка синтаксиса'
        case 'ZeroDivisionError':
            return 'ошибка деления на ноль'
        case 'FileNotFoundError':
            return 'файл или каталог не найден'
    return 'неизвестная ошибка'


def _get_message(err_type: str, message: str) -> str:
    """Возвращает русский текст сообщения ошибки."""
    match err_type:
        case 'NameError':
            if re.match(r"name '\w+' is not defined.", message) is not None:
                name = message[6: message.rfind("'")]
                return f"имя '{name}' не определено"
        case 'TypeError':
            if re.match(r"unsupported operand type\(s\) for [+\-*/|&^]: '\w+' and '\w+'", message) is not None:
                operator = message[32: 33]
                operand1 = message[message.find("'") + 1: message.find("'", message.find("'") + 1)]
                operand2 = message[47: message.rfind("'")]
                return f"неподдерживаемый оператор {operator} для типов '{operand1}' и '{operand2}'"
        case 'SyntaxError':
            if message == 'invalid syntax':
                return 'неправильно написана строка'
            elif message == "'return' outside function":
                return "ключевое слово 'return' вне функции"
            elif message == "'break' outside loop":
                return "ключевое слово 'break' вне цикла"
            elif message == "'continue' not properly in loop":
                return "ключевое слово 'continue' вне цикла"
        case 'ZeroDivisionError':
            return 'на ноль делить нельзя'
        case 'FileNotFoundError':
            return f'{message[38:-1]}'
    return 'неизвестная ошибка'
