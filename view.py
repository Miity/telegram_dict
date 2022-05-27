import requests
import json
import time
from dictionary import *
from secret import URL


def write_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, 
            indent=2, ensure_ascii = False)

def load_json(filename):
    with open(filename) as json_data:
        json_data = json.load(json_data)
    return json_data

def get_updates(offset = None):
    url = URL + "getUpdates"
    if offset:
        r = requests.get(url, params = {'offset': offset })
    else:
        r = requests.get(url)
    return r.json()

def is_new_updates(r, update_id):
    if 'result' not in r:
        return False
    elif r['result'][-1]['update_id'] != update_id:
        update_id = r['result'][-1]['update_id']
        return True
    elif update_id == r['result'][-1]['update_id']:
        return False

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
    text = user_req['message']['text']

    if text == '/stop':
        text = "Добре, бувай. Побачемось іншим разом."
        send_message(user_hist, text)

    elif text == '/start':
        text = "Привіт, я допоможу тобі запам'ятати нові слова. \n\nВідправляй всі слова, що хочеш перекласти, я запишу їх до словника. \n\nТи можешь подивитись свій словник, відправ мені команду /show \n\nБільше команд, ти знайдеш у меню знизу."
        send_message(user_hist, text)

    elif text == '/help':
        text = '/start \n /stop \n /show \n /del /d'
        send_message(user_hist, text)

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
        send_message(user_hist, text=translate)





