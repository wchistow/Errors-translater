def translate_message(err_message: list[str]) -> str:
    """Возвращает русский текст ошибки."""
    err_message = err_message[1:]
    result = f'{_get_location(err_message[0]).capitalize()}:\n  {err_message[1]}\n{_get_message(err_message[2])}'
    return result


def _get_location(location: str) -> str:
    """Возвращает русский текст места ошибки."""
    file = location[6:location.rfind('"')]
    line = location[location.find(',') + 7: location.rfind(',')]
    return f'в файле "{file}", строке {line}'


def _get_message(message: str) -> str:
    """Возвращает русский текст сообщения ошибки."""
    err_type = message[:message.find(':')]
    return f'{_get_error_type(err_type).capitalize()}: '


def _get_error_type(err_type: str) -> str:
    """Возвращает русский перевод типа ошибки."""
    match err_type:
        case 'NameError':
            return 'ошибка имени'
