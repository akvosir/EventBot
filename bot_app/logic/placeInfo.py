def parse_time(time):
    str = time[:5]
    return str


def parse_len(length):
    formating = float(length)
    to_str = 'в ' + str(formating) + ' км от вас'
    return to_str


def parse_search_text(message):
    time = message['w_from'][:5]
    place = '<b>' + message['name'] + '</b>\n' + \
            '👌🏻' + message['place'] + '\n' \
                                        '🚖 ' + message['address'] + '\n' \
                                         '🕒 Начинается в ' + time + '\n' + \
            '📞' + str(message['phone']) + '\n' + message['text'] + '\n'
    if message.get('length', None) != None:
        length = parse_len(message['length'])
        place += '🏃' + length
    return place
