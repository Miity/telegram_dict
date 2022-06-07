from dictionary import *
from utils import *


def send_message(user, **kwargs):
    url = URL + 'sendMessage'
    answer = {'chat_id': user.chat_id }
    for x,y in kwargs.items():
        answer[x] = y
    r = requests.post(url, json = answer)
    print(answer)


def make_response(user, user_hist, dictionary):
    user_req=user_hist['result'][-1]
    text = user_req['message']['text']

    if text == '/settings':
        reply_markup = {'keyboard':[
                    [{'text':'choose language for dictionary'}],
                    [{'text':'delete keyboard'}]
                    ]}

        remove_keyboard = {'remove_keyboard': True}
        send_message(user, text=text, reply_markup=reply_markup)
        

    elif text in ('uk','en', 'it', 'ge'):
        user.update(dict_language = text)
        remove_keyboard = {'remove_keyboard': True}
        send_message(user, text="ви вибрали язик {}".format(text),reply_markup=remove_keyboard )


    elif text == 'choose language for dictionary':
        text = 'Виберіть на яку мову перекладати?'
        reply_markup = {'keyboard':[
                    [{'text':'uk'},{'text':'en'}],
                    [{'text':'it'},{'text':'ge'}]
                    ]}
        send_message(user, text = text, reply_markup=reply_markup)


    elif text == '/start':
        text = "Привіт, я допоможу тобі запам'ятати нові слова. \n\nВідправляй всі слова, що хочеш перекласти, я запишу їх до словника. \n\nТи можешь подивитись свій словник, відправ мені команду /show \n\nБільше команд, ти знайдеш у меню знизу."
        send_message(user, text=text)

    elif text == '/show':
        send_message(user, text=dictionary.show_all_words())
            
    else:
        translate = translation(text, user.dict_language)
        dictionary.add_word({text:translate})
        send_message(user, text=translate)





