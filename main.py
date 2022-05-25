import time
from view import *
import json


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
    if r['result'][-1]['update_id'] != update_id:
        update_id = r['result'][-1]['update_id']
        return True
    elif update_id == r['result'][-1]['update_id']:
        return False


def main():
    r = get_updates()
    with open('json/answer.json', 'w') as f:
        json.dump(r, f, 
            indent=2, ensure_ascii = False)
    
    update_id = r['result'][-1]['update_id']

    while True:

        while is_new_updates(r, update_id) == False:
            time.sleep(2)
            if len(r['result']) > 10:
                r = get_updates(offset = r['result'][-1]['update_id'])
                print('offset > 10') 
            else:
                r = get_updates()
            
        update_id = r['result'][-1]['update_id']
        print('we have new update')

        last_r = r['result'][-1]
        user_id = r['result'][-1]['message']['from']['id']

        # визначемо чи це новий юзер?
        # якщо новий, то робимо файли під нього 
        # і добавляємо до бази
        with open('user_data/users.json') as json_data:
            users = json.load(json_data)
        users_id = []
        for i in users['users']:
            users_id.append(i['id'])

        if user_id not in users_id:
            # добавляємо до знайомих юзерів
            with open('user_data/users.json', 'w') as f:
                users['users'].append(r['result'][-1]['message']['from'])
                json.dump(users, f, 
                    indent=2, ensure_ascii = False)

            # new User History
            filename = 'user_data/' + str(user_id) +'_hist.json'
            with open(filename, 'w') as f:
                user_data = {'result':[]}
                user_data['result'].append(last_r)
                json.dump(user_data, f, 
                    indent=2, ensure_ascii = False)

            # new User dict
            filename = 'user_data/' + str(user_id) +'_dict.json'
            with open(filename, 'w') as f:
                dic = {'words':{}}
                json.dump(dic, f, 
                    indent=2, ensure_ascii = False)
        else:
            #загружаємо та перезаписуємо історію юзера
            filename = 'user_data/' + str(user_id) +'_hist.json'
            user_data = load_json(filename)
            with open(filename, 'w') as f:
                user_data['result'].append(last_r)
                json.dump(user_data, f, indent=2, ensure_ascii = False )
            

        # загружаємо останні данні
        user_hist = load_json('user_data/' + str(user_id) +'_hist.json')
        #загружаємо словарь юзера
        dic = load_json('user_data/' + str(user_id)+'_dict.json')

        #вибираємо режим
        mode = None
        '''
        try:
            if user_hist['result'][-2]['message']['text'] == '/del':
                mode = 'del'
        except:
            pass
        '''
        if mode == 'del':
            send_message(user_hist, 
            text='Я ще не вмію')
            words=dic['words']

        else:
            make_response(user_hist, dic) 

        

if __name__ == "__main__":
    main()
