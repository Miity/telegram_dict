from datetime import datetime
import time
from view import *


def main():
    r = get_updates()
    write_json(r,'json/answer.json')

    update_id = r['result'][-1]['update_id']

    users = load_json('user_data/users.json')
    users_id = []
    for i in users['users']:
        users_id.append(i['id'])
    s = None
    while True:
        #чекаємо на новий запит
        while is_new_updates(r, update_id) == False:
            time.sleep(2)
            if len(r['result']) > 10:
                r = get_updates(offset = r['result'][-1]['update_id'])
                print('offset > 10') 
            else:
                if s:
                    if time.time() >= s["time"]+60:
                        s["time"]+=60
                        text='пройшла 1 хвилина'
                        chat_id = s['user_id']
                        url = URL + 'sendMessage'
                        answer = {'chat_id': chat_id, 'text': text}
                        r = requests.post(url, json = answer)  
                r = get_updates()   
        update_id = r['result'][-1]['update_id']

        
        # визначемо чи це новий юзер?
        # якщо новий, то робимо файли під нього 
        # і добавляємо до бази
        last_r = r['result'][-1]
        user_id = r['result'][-1]['message']['from']['id']
        if user_id not in users_id:
            # добавляємо до знайомих юзерів
            users_id.append(user_id)
            filename = 'user_data/users.json'
            data = users['users'].append(r['result'][-1]['message']['from'])
            write_json(data, filename)

            # new User Data
            filename = 'user_data/' + str(user_id) +'_data.json'
            data = {'result':{'user_id':user_id, 'mode':None, 'mode_step':None}}
            write_json(data, filename)

            # new User History
            filename = 'user_data/' + str(user_id) +'_hist.json'
            data = {'result':[last_r,]}
            write_json(data, filename)

            # new User dict
            filename = 'user_data/' + str(user_id) +'_dict.json'
            data = {'words':{}}
            write_json(data, filename)
        else:
            #загружаємо та перезаписуємо історію юзера
            filename = 'user_data/' + str(user_id) +'_hist.json'
            data = load_json(filename)
            data['result'].append(last_r)
            write_json(data, filename)

        # загружаємо останні данні
        #загружаємо словарь юзера
        user_hist = load_json('user_data/' + str(user_id) +'_hist.json')
        user_data = load_json('user_data/' + str(user_id) +'_data.json')
        dic = load_json('user_data/' + str(user_id)+'_dict.json')




        #вибираємо режим
        #видалення
        #вивчення( добавити до навчання)
        if len(user_hist['result'])>=2:
            if user_hist['result'][-1]['message']['text'] == '/delete':
                user_data['result']['mode'] = 'delete'
                user_data['result']['mode_step'] = int(1)
                filename = 'user_data/' + str(user_id) +'_data.json'
                write_json(user_data, filename)
            elif user_hist['result'][-1]['message']['text'] == '/study':
                mode = 'study'
            elif user_hist['result'][-1]['message']['text'] == '/stop_study':
                mode = 'stop_study'
            elif user_hist['result'][-1]['message']['text'] == '/settings':
                mode = 'settings'

        # обробляємо режими
        if user_data['result']['mode'] == "delete":
            if user_data['result']['mode_step'] == 1:
                print('delete mode step 1')
                text = 'Який номер хочешь видалити?'
                send_message(user_hist, text)
                show_all_words(user_hist, dic)

                user_data['result']['mode_step'] = int(2)
                filename = 'user_data/' + str(user_id) +'_data.json'
                write_json(user_data, filename)

            elif user_data['result']['mode_step'] == 2:
                print('delete mode step 2')
                try: 
                    #видаляємо по індексу
                    i = int(user_hist['result'][-1]['message']['text'])
                    l = []
                    for x,y in dic['words'].items():
                        l.append(x)
                    word = l[i]
                    dic['words'].pop(word)

                    # update User dict
                    filename = 'user_data/' + str(user_id) +'_dict.json'
                    write_json(dic,filename)
                    send_message(user_hist, text='я видалив: ' + word)

                    #скидаємо mode
                    user_data['result']['mode'] = None
                    user_data['result']['mode_step'] = None
                    filename = 'user_data/' + str(user_id) +'_data.json'
                    write_json(user_data, filename)

                except:
                    print('index not find')
                    make_response(user_hist, dic) 
                    user_data['result']['mode'] = None
                    user_data['result']['mode_step'] = None
                    filename = 'user_data/' + str(user_id) +'_data.json'
                    write_json(user_data, filename)
        elif user_data['result']['mode'] == "study":
            print("study mode")
            now = time.time() 
            print(now)
            s = {"user_id": user_id, "time":now}

        else:
            make_response(user_hist, dic) 

        

if __name__ == "__main__":
    main()
