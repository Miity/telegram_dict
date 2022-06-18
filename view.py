from time import time

def errore(bot, user):
	remove_keyboard = {'remove_keyboard': True}
	bot.send_message(user, text="try again",reply_markup=remove_keyboard )
	user.reset()

def delete(bot, user, dictionary):
	if user.mode_step == 1:
		bot.send_message(user, text='Який номер хочешь видалити?')
		bot.send_message(user, text=dictionary.show_all_words())
		user.update(mode_step=2)
	elif user.mode_step == 2:
	    try:
	        # видаляємо по індексу
	        dictionary.del_word(int(bot.text))
	        user.reset()
	    except:
	        print('index not find')
	        user.reset()

def study(bot, user):
	if user.mode_step == 1:
	    bot.send_message(
	        user, text='Окей, я буду відправляти вам одне із слів')
	    bot.send_message(user, text='Як часто відправляти?')
	    bot.send_message(user, text='напишіть раз у скільки хвилин')
	    user.update(mode_step=2)

	elif user.mode_step == 2:
	    try:
	        now = time()
	        minutes = int(bot.text)
	        sec = minutes * 60
	        user.update(mode_step=3, start_time=now, wait_time=sec)

	    except Exception as e:
	    	print('errore in study step 2') 
	    	print(e)

def settings(bot, user):
	if user.mode_step == 1:
		reply_markup = {'keyboard':[
		            [{'text':'choose language for dictionary'}],
		            [{'text':'delete keyboard'}]
		            ]}
		bot.send_message(user, text='what do you want?', reply_markup=reply_markup)
		user.update(mode_step=2)

	elif user.mode_step == 2:
		if bot.text == 'choose language for dictionary':
		    text = 'Виберіть на яку мову перекладати?'
		    reply_markup = {'keyboard':[
		                [{'text':'uk'},{'text':'en'}],
		                [{'text':'it'},{'text':'ge'}]
		                ]}
		    bot.send_message(user, text = text, reply_markup=reply_markup)
		    user.update(mode_step=3)
		else:
			errore(bot, user)

	elif user.mode_step == 3:	
		if bot.text in ('uk','en', 'it', 'ge'):
			user.update(dict_language = bot.text)
			remove_keyboard = {'remove_keyboard': True}
			bot.send_message(user, text="ви вибрали язик {}".format(bot.text),reply_markup=remove_keyboard )
			user.reset()
		else:
			errore(bot, user)
















