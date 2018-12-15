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
        help_button(chat_id, '📢 Привет!'
                        ' Oтправляй локацию или выбирай категорию и'
                             'я покажу тебе интересные события рядом и в ближайшее время!👇 ')
        timer = threading.Timer(30, send_notification)
        thread_store.link_store[chat_id] = timer
        timer.start()
    elif message == '/help':
        help_button(chat_id, "жми кнопкууууу")
    else:
        return 1
    return 0


def print_off_location(chat_id):
    bot.sendMessage(chat_id, 'Включи геолокацию :)')
