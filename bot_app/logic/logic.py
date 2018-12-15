import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot_app.logic.placeInfo import parse_search_text
from bot_app.logic.send_location import button_request, location_request
from bot_app.configs.config import TOKEN

words = {"concert": "концерт",
         "lection": "лекция",
         "theatre": "театр",
         "stand-up": "стендап",
         "сlasses": "мастер-клас"
         }
bot = telegram.Bot(TOKEN)


def send_category(id, callback):
    if callback in words.keys():
        response = button_request(words[callback])
        send_results(response, id)
    else:
        print('ok')


def send_location(id, lat, long):
    response = location_request(lat, long)
    send_results(response, id)

def send_results(offers, id):
    k = 0
    if offers == '()':
        no_search_result(id)
    else:
        k = 0

        for i in offers:  # сaption = parse_search_text(i)
            k = k + 1
            if k == len(offers):
                help_button(id, text=parse_search_text(i))
                break
            bot.sendMessage(id, text=parse_search_text(i), parse_mode='HTML',
                            disable_web_page_preview=True,
                            timeout=40)


def sorry_message(id):
    bot.sendSticker(id, 'CAADAgADmgADBiTKB2XXWjd_6tUOAg')
    help_button(id, 'Не умею распознавать слова! Попробуй отправить локацию или выбрать категорию.👇🏻')


def help_button(chat_id, text):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Концерт 🎼", callback_data="concert")],
        [InlineKeyboardButton("Лекция 📚", callback_data="lection")],
        [InlineKeyboardButton("Театр 🎭", callback_data="theatre")],
        [InlineKeyboardButton("Стендап 👁", callback_data="stand-up")],
        [InlineKeyboardButton("Мастер-класс 🎨", callback_data="classes")]

    ])
    bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard, parse_mode='HTML')


def no_search_result(chat_id):
    bot.sendSticker(chat_id, 'CAADAgADzlsAAmOLRgyykJdaDfyaHwI')
