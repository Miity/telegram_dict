from datetime import datetime
import time
from view import *
import random
from models import User, Dictionary
from utils import *


def main():
    r = get_updates()
    write_json(r,'json/answer.json')
    update_id = r['result'][-1]['update_id']

    while True:
        #чекаємо на новий запит
        while is_new_updates(r, update_id) == False:
            time.sleep(2)

            if len(r['result']) > 10:
                r = get_updates(offset = r['result'][-1]['update_id'])

            else:
                #якщо режим навчання
                users = load_json('user_data/users.json')
                for user in users['users']:
                    user = User(user['id'])
                    if user.mode == 'study' and user.mode_step == 3:
                        print('study mode: ', user.id)
                        print('time to send:', time.time()-user.start_time)
                        if time.time() >= user.start_time + user.wait_time:
                            user.update(start_time=time.time())
                            #відправляємо рандомне слово
                            dictionary = Dictionary(user.id).open()
                            x,y = random.choice(list(dictionary["words"].items()))
                            send_message(user, x + ' - ' + y)

                r = get_updates()   

        update_id = r['result'][-1]['update_id']

        

        # дістаємо інфу з телеграмму
        last_r = r['result'][-1]
        user_id = r['result'][-1]['message']['from']['id']
        user_chat_id = r['result'][-1]['message']['chat']['id']

        # ініціалізуємо юзера та його словарь
        last_r = r['result'][-1]
        user_id = r['result'][-1]['message']['from']['id']
        user = User(user_id)
        user.update(chat_id=user_chat_id)
        user.rewrite_hist(last_r)
        dictionary = Dictionary(user_id)

        # загружаємо останні данні
        user_hist = load_json('user_data/' + str(user.id) +'_hist.json')
        user_dic = dictionary.open()

        #вибираємо режим
        if user_hist['result'][-1]['message']['text'] == '/delete':
            user.update(mode='delete', mode_step=1)
        elif user_hist['result'][-1]['message']['text'] == '/study':
            user.update(mode='study', mode_step=1)
        elif user_hist['result'][-1]['message']['text'] == '/stop_study':
            user.reset()
        elif user_hist['result'][-1]['message']['text'] == '/settings':
            user.update(mode='settings')

        # обробляємо режими
        if user.mode == "delete":
            if user.mode_step == 1:
                send_message(user, 'Який номер хочешь видалити?')
                send_message(user, dictionary.show_all_words())
                user.update(mode_step=2)
            elif user.mode_step == 2:
                try: 
                    #видаляємо по індексу
                    i = int(user_hist['result'][-1]['message']['text'])
                    dictionary.del_word(i)
                    user.reset()
                except:
                    print('index not find')
                    make_response(user, user_hist, user_dic) 
                    user.reset()

        elif  user.mode == "study" and user.mode_step < 3:
            if user.mode_step == 1:
                print("study mode")
                send_message(user, text='Окей, я буду відправляти вам одне із слів')
                send_message(user, text='Як часто відправляти?')
                send_message(user, text='напишіть раз у скільки хвилин')
                user.update(mode_step=2)
            elif user.mode_step == 2:
                try:
                    now = time.time() 
                    minutes = int(user_hist['result'][-1]['message']['text'])
                    sec = minutes * 60
                    user.update(mode_step = 3, start_time=now, wait_time=sec)
                except:
                    # 
                    pass

        else:
            make_response(user, user_hist, dictionary) 

        

if __name__ == "__main__":
    main()