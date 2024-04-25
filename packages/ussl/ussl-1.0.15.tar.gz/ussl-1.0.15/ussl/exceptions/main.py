import json
from typing import List, Union


class SOARException(Exception):
    """
    Стандартный класс для исключений скриптов.

    Приватные поля:
        ``_return_code``(int): код возврата
        ``_TEMPLATE``(str): шаблон сообщения

    Публичные поля и свойства:
        ``message``(Union[List[str], str, dict]): информация об исключении
        ``return_code``(int): код возврата
    """
    _return_code: int = 1
    _TEMPLATE: str = 'Error: {args}.'

    message: str = None

    @property
    def return_code(self):
        return self._return_code

    def __init__(self, message: Union[List[str], str, dict, Exception]):
        if message is None:
            self.message = ' '
        if isinstance(message, Exception):
            self.message = str(message)
        elif isinstance(message, list):
            self.message = ', '.join(message)
        elif isinstance(message, dict):
            self.message = json.dumps(message)
        elif isinstance(message, str):
            self.message = message
        else:
            raise TypeError('Message must be str, list, dict or Exception')

    def __str__(self):
        return self._TEMPLATE.format(args=self.message)
