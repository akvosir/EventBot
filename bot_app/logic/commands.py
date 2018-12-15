import threading
import re
import telegram
from flask import copy_current_request_context
from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

from bot_app.configs.config import TOKEN
from bot_app.logic import thread_store

bot = telegram.Bot(TOKEN)


def print_command(chat_id, message):
    @copy_current_request_context
    def send_notification():
        bot.sendMessage(chat_id,
                        'Проблемы? Жми /help ✌️️')

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📍 Отправить местоположение", request_location=True)]],
        resize_keyboard=True)

    timer = thread_store.link_store.get(chat_id)
    if timer is not None:
        timer.cancel()

    if message == '/start':
        bot.sendMessage(chat_id,
                        '📢 Привет!'
                        ' Oтправляй локацию или выбирай категорию и'
                        'я покажу тебе интересные события рядом и в ближайшее время!👇 ',
                        reply_markup=keyboard)
        help_button(chat_id)
        timer = threading.Timer(30, send_notification)
        thread_store.link_store[chat_id] = timer
        timer.start()
    elif message == '/help':
        help_button(chat_id)
    elif re.findall(r'\w \w', message):
        bot.sendMessage(chat_id, 'Я ще не вмію розпізнавати більше одного слова, вибач.')
    else:
        return 1
    return 0


def print_off_location(chat_id):
    bot.sendMessage(chat_id, 'Схоже на те, що геолокація на смартфоні виключена. Будь-ласка, увімкни її, щоб я зміг '
                             'знайти пропозиції для тебе.:)')


def help_button(chat_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Концерт 🎼", callback_data="concert")],
        [InlineKeyboardButton("Лекция 📚", callback_data="lection")],
        [InlineKeyboardButton("Театр 🎭", callback_data="theatre")],
        [InlineKeyboardButton("Стендап 👁", callback_data="stand-up")],
        [InlineKeyboardButton("Мастер-класс 🎨", callback_data="classes")]

    ])
    bot.send_message(chat_id=chat_id, text='Куда хочешь пойти?', reply_markup=keyboard)
