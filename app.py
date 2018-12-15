from pprint import pprint

import telegram
from flask import Flask
from flask import jsonify
from flask import request
from telegram.error import TimedOut, NetworkError, RetryAfter

from bot_app.configs.config import TOKEN
from bot_app.logic import thread_store
from bot_app.logic.commands import print_command, print_off_location
from bot_app.logic.logic import send_category

app = Flask(__name__)
app.config.from_object('bot_app.configs.config')
bot = telegram.Bot(TOKEN)


# ddd


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        pprint(r)
        try:
            if 'callback_query' in r.keys(): # more button
                send_category(r['callback_query']['from']['id'], r['callback_query']['data'])
                print("OLOLO")
            elif 'edited_message' in r.keys(): # wtf
                print('OK')
            elif 'location' in r['message'].keys(): # if location
                chat_id = r['message']['chat']['id']
                bot.sendSticker(chat_id, 'CAADAgADmgADBiTKB2XXWjd_6tUOAg')
                bot.sendMessage(chat_id, 'А вы знаете как закрыть сессию на АУТСе!', parse_mode='HTML', disable_web_page_preview=True, timeout=40)
            elif 'text' in r['message']: # text case
                chat_id = r['message']['chat']['id']
                if print_command(chat_id, r['message']['text']):
                    bot.sendSticker(chat_id, 'CAADAgADmgADBiTKB2XXWjd_6tUOAg')
                    bot.sendMessage(chat_id, 'А вы знаете как закрыть сессию на АУТСе!', parse_mode='HTML',
                                    disable_web_page_preview=True, timeout=40)
                print('OK')
        except (TimedOut, NetworkError, RetryAfter) as e:
            print(e)
        # except Exception as e:
        #    # print(e)

        return jsonify(r)
    return 'Bot bot bot ohoho!'

# https://api.telegram.org/bot670691033:AAEVXVMJKp2TQKMqLLGpj0VObuOqr2wfGFk/setWebhook?url=https://1bbc8ec1.ngrok.io
if __name__== '__main__':
    app.run(debug=True, port=5000)
