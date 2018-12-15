import telegram

from bot_app.logic.placeInfo import parse_search_text
from bot_app.logic.send_location import button_request
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


def send_results(offers, id):
    k = 0
    if offers == '()':
        no_search_result(id)
    else:
        for i in offers:  # сaption = parse_search_text(i)
            bot.sendMessage(id, text=parse_search_text(i), parse_mode='HTML',
                            disable_web_page_preview=True,
                            timeout=40)


def no_search_result(chat_id):
    bot.sendSticker(chat_id, 'CAADAgADzlsAAmOLRgyykJdaDfyaHwI')
    bot.sendMessage(chat_id, 'Упс! Актуальных событий нет, но они когда-то появятся, зайди в другое время.')
