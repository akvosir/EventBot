from pprint import pprint

import telegram
from flask import Flask
from flask import jsonify
from flask import request
from telegram.error import TimedOut, NetworkError, RetryAfter

from bot_app.configs.config import TOKEN
from bot_app.logic import thread_store
from bot_app.logic.commands import print_command, print_off_location
from bot_app.logic.logic import send_category, send_location, sorry_message

app = Flask(__name__)
app.config.from_object('bot_app.configs.config')
bot = telegram.Bot(TOKEN)



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
                chat_id = r['message']['chat']['id']  # type: object
                latitude = r['message']['location']['latitude']
                longitude = r['message']['location']['longitude']
                send_location(chat_id, latitude, longitude)
            elif "text" in r['message']:
                chat_id = r['message']['chat']['id']
                if print_command(chat_id, r['message']['text']):
                    sorry_message(chat_id)
                print('OK')
        except (TimedOut, NetworkError, RetryAfter) as e:
            print(e)
        except Exception as e:
            print(e)

        return jsonify(r)
    return 'Bot bot bot ohoho!'

if __name__== '__main__':
    app.run(debug=True, port=5000)
