import requests
import json
import time
from dictionary import *
from secret import URL


def read_text(r):
    text = r['message']['text']
    return text 

def send_message(r, text):
    chat_id = r['result'][-1]['message']['chat']['id']
    url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json = answer)

def show_all_words(user_hist, dic):
    words = ''
    j=0
    for i in dic['words']: 
        word = str(j) + '. ' + i+' - '+ dic['words'][i] + "\n"
        words = words + word
        j+=1
    send_message(user_hist, words)




def make_response(user_hist, dic):
    user_req=user_hist['result'][-1]
    text = read_text(user_req)

    if text == '/stop':
        print('stop!!!')
        text = "Окей, увидимся в другой раз"
        send_message(user_hist, text)

    elif text == '/start':
        print('start')
        text = "Окей, давай начнем. Я загрузил ваш словарь"
        send_message(user_hist, text)

    elif text == '/help':
        text = '/start \n /stop \n /show \n /del /d'
        send_message(user_hist, text)

    elif text == '/delete':
        text = 'какой номер вы хотите удалить?'
        send_message(user_hist, text)
        show_all_words(user_hist, dic)

    elif text == '/show':
        show_all_words(user_hist, dic)
            
    else:
        translate = translation(text)
        dic['words'][text]=translate
        print(dic)

        filename = 'user_data/' + str(user_hist['result'][-1]['message']['from']['id']) +'_dict.json'
        with open(filename, 'w') as f:
            json.dump(dic, f, 
                indent=2, ensure_ascii = False)

        send_message(user_hist, 
            text='я добавлю это в твой словарь: ' + translate)





