from dictionary import *
from utils import *


def send_message(user, text):
    url = URL + 'sendMessage'
    answer = {'chat_id': user.chat_id, 'text': text}
    r = requests.post(url, json = answer)


def make_response(user, user_hist, dictionary):
    user_req=user_hist['result'][-1]
    text = user_req['message']['text']

    if text == '/stop':
        text = "Добре, бувай. Побачемось іншим разом."
        send_message(user, text)

    elif text == '/start':
        text = "Привіт, я допоможу тобі запам'ятати нові слова. \n\nВідправляй всі слова, що хочеш перекласти, я запишу їх до словника. \n\nТи можешь подивитись свій словник, відправ мені команду /show \n\nБільше команд, ти знайдеш у меню знизу."
        send_message(user, text)

    elif text == '/help':
        text = '/start \n /stop \n /show \n /del /d'
        send_message(user, text)

    elif text == '/show':
        send_message(user, dictionary.show_all_words())
            
    else:
        translate = translation(text)
        dictionary.add_word({text:translate})
        send_message(user, text=translate)





