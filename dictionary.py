from googletrans import Translator


translator = Translator()

def translation(text, dest='en'):
    translation = translator.translate(text, dest)
    return translation.text


# вибираємо мову для перекладу, та підставляємо 
# правильний код мови
def chois_lang(lg):
	languages = {
				'en':['english', 'en' ], 
				'uk': ['ukraine', 'uk' ],
				'it': ['italian', 'it' ]
				}
	for x,y in languages.items():
		if str(lg)==x:
			return str(x)
		elif str(lg) in y:
			return str(x)
		else:
			continue
	
	return print('Sorry, I didnt find this languege')


def translation_choise(text, lang):
	translation = translator.translate(text, dest=lang)
	return translation.text


def add_word(dic, word):
	dic[word]=translate(word)
	pass

def del_word(dic, index):
	pass

def show_all_words(dic):
	pass

def read_json():
	pass

def write_json():
	pass

