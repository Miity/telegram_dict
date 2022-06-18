from time import time, sleep
import random
from my_telegram import BOT
from models import User, Dictionary
from utils import load_json
from secret import token
from view import *
from dictionary import translation


def main():
    if bot.is_new_updates():

        # дістаємо інфу з телеграмму
        user_id = bot.updates['result'][-1]['message']['from']['id']
        user_chat_id = bot.updates['result'][-1]['message']['chat']['id']

        # ініціалізуємо юзера та його словарь
        user = User(user_id)
        user.update(chat_id=user_chat_id)
        user.rewrite_hist(bot.updates['result'][-1])
        dictionary = Dictionary(user.id, user.dict_language)

        # обробляємо запит
        if bot.text in ('/delete', '/study', '/start', '/settings', '/stop_study', '/show'):
            user.update(mode=bot.text, mode_step=1)

        if user.mode == "/delete":
            delete(bot, user, dictionary)

        elif user.mode == "/study" and user.mode_step < 3:
            study(bot, user)

        elif user.mode == '/stop_study':
            user.reset()

        elif user.mode == "/settings":
            settings(bot, user)

        elif user.mode == '/start':
            text = "Привіт, я допоможу тобі запам'ятати нові слова. \n\nВідправляй всі слова, що хочеш перекласти, я запишу їх до словника. \n\nТи можешь подивитись свій словник, відправ мені команду /show \n\nБільше команд, ти знайдеш у меню знизу."
            bot.send_message(user, text=text)

        elif bot.text == '/show':
            bot.send_message(user, text=dictionary.show_all_words())

        else:
            translate = translation(bot.text, user.dict_language)
            dictionary.add_word({bot.text: translate})
            bot.send_message(user, text=translate)

    else:
        users = load_json('user_data/users.json')
        for user in users['users']:
            user = User(user['id'])
            if user.mode == 'study' and user.mode_step == 3:
                if time.time() >= user.start_time + user.wait_time:
                    user.update(start_time=time.time())
                    # відправляємо рандомне слово
                    dictionary = Dictionary(user.id).open()
                    x, y = random.choice(list(dictionary["words"].items()))
                    bot.send_message(user, text=x + ' - ' + y)
        sleep(2)


if __name__ == "__main__":
    bot = BOT(token)
    while True:
        main()
