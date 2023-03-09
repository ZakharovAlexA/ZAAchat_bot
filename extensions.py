import requests
import json
from config import keys


class APIException(Exception):
    pass


class Converters:
    """ Класс конвертора. Выполняет обращение к API и отрабатывает ошибки ввода."""
    @staticmethod
    def get_price(value):

        if len(value) != 3:
            raise APIException('Количество вводимых параметров должно равняться трём!')

        base, quote, amount = value
        base = base.lower()         # убираем зависимость от регистра - приводим всё к нижнему регистру.
        quote = quote.lower()

        try:
            keys[base]
        except KeyError:
            raise APIException(f'Валюта "{base}" не может быть обработана! \n'
                               f'Список поддерживаемых валют можно посмотреть командой /values')

        try:
            keys[quote]
        except KeyError:
            raise APIException(f'Валюта "{quote}" не может быть обработана! \n'
                               f'Список поддерживаемых валют можно посмотреть командой /values')

        if base == quote:
            raise APIException('Введите разные валюты!')

        try:
            float(amount)
        except ValueError:
            raise APIException(f'Не удалось обрабоать количество: {amount}')

        res = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={keys[base]}&tsyms={keys[quote]}')
        total = json.loads(res.content)[keys[quote]] * float(amount)
        return total
