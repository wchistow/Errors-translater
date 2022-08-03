def translate_message(err_message: list[str]) -> str:
    """Возвращает русский текст объяснения ошибки."""
    err_message = err_message[1:]

    result = f'{_get_location(err_message[0]).capitalize()}:\n  {err_message[1]}'

    return result


def _get_location(location: str) -> str:
    """Возвращает русский текст объяснения места ошибки."""
    file = location[6:location.rfind('"')]
    line = location[location.find(',') + 7: location.rfind(',')]

    return f'в файле "{file}", строке {line}'
