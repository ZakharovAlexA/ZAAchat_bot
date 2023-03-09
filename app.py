""" Telegram Бот для работы с конвертацией валют."""
__author__ = 'Захаров Александр А.'

import telebot
from config import *

from extensions import Converters, APIException

bot = telebot.TeleBot(APITOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Добро пожаловать, {message.chat.first_name}! \n"
                                      f"Для конвертации введите данные в формате: \n"
                                      f"(цена интересуемой валюты) (в какой валюте) "
                                      f"(количество конвертируемой валюты) \n"
                                      f"Пример: биткоин доллар 1 \n"
                                      f"Список поддерживаемых валют можно посмотреть командой /values")


@bot.message_handler(commands=['values'])
def send_value(message):
    text = 'Список поддерживаемых валют:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        val = message.text.split(' ')
        total_res = Converters.get_price(val)
        base, quote, amount = val
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя \n {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось отработать команду \n {e}')
    else:
        text = f'Цена {amount} {base} в {quote} = {total_res}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
