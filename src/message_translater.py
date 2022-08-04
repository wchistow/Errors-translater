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
    return 'неизвестная ошибка'


def _get_message(err_type: str, message: str) -> str:
    """Возвращает русский текст сообщения ошибки."""
    match err_type:
        case 'NameError':
            if re.match(r"name '\w+' is not defined.", message) is not None:
                name = message[6: message.rfind("'")]
                return f"имя '{name}' не определено"
    return 'неизвестная ошибка'
