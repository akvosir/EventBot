import threading
import re
import telegram
from flask import copy_current_request_context
from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

from bot_app.configs.config import TOKEN
from bot_app.logic import thread_store
from bot_app.logic.logic import help_button

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
        bot.send_message(chat_id=chat_id, text='📢 Привет!'
                        ' Oтправляй локацию или выбирай категорию и'
                                               'я покажу тебе интересные события рядом и в ближайшее время!',
                         reply_markup=keyboard, parse_mode='HTML', disable_web_page_preview=True, )
        help_button(chat_id, 'Выбери категорию:')
        timer = threading.Timer(30, send_notification)
        thread_store.link_store[chat_id] = timer
        timer.start()
    elif message == '/help':
        help_button(chat_id, "Выбери категорию:")
    else:
        return 1
    return 0


def print_off_location(chat_id):
    bot.sendMessage(chat_id, 'Включи геолокацию :)')


def help_button(chat_id, text):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Концерт 🎼", callback_data="concert")],
        [InlineKeyboardButton("Лекция 📚", callback_data="lection")],
        [InlineKeyboardButton("Театр 🎭", callback_data="theatre")],
        [InlineKeyboardButton("Стендап 👁", callback_data="stand-up")],
        [InlineKeyboardButton("Мастер-класс 🎨", callback_data="classes")]

    ])
    bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard, parse_mode='HTML',
                     disable_web_page_preview=True, )
