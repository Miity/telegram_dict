from utils import load_json, write_json

user_directory = "user_data/"


class User(): 
  def __init__(self, id):
    global index
    data = load_json(user_directory+'users.json')
    find = False
    index = 0
    for i in data['users']:
      if i['id'] == id:
        self.id = i['id']
        for x,y in i['data'].items():
          setattr(self, x, y)
        find = True
        break
      else:
        index+=1

    if find == False:
      self.id = id
      self.mode = None
      write_json(data = {'result':[]}, filename=user_directory + str(self.id) + '_hist.json')
      user = {'id':self.id,
              'data':{
                'mode':None,
                'mode_step':None,    
                }
              }
      data['users'].append(user)
      index=len(data['users'])-1
      write_json(data=data,filename=user_directory+'users.json')

  def update(self, *args, **kwargs):
    filename = user_directory+'users.json'
    data = load_json(filename)
    if kwargs:
      for x,y in kwargs.items():
        data['users'][index]['data'][x]=y 
    write_json(data, filename)

    for x,y in data['users'][index]['data'].items():
        setattr(self, x, y)

  def reset(self):
    self.mode = None
    self.mode_step = None
    filename = user_directory+'users.json'
    data = load_json(filename)
    data['users'][index]['data']['mode'] = self.mode
    data['users'][index]['data']['mode_step'] = self.mode_step
    write_json(data, filename)

  def rewrite_hist(self, new_data):
    filename = 'user_data/' + str(self.id) +'_hist.json'
    data = load_json(filename)
    data['result'].append(new_data)
    write_json(data, filename)


class Dictionary():
  def __init__(self, id):
    self.owner_id = id
    self.filename = str(self.owner_id) +'_dict.json'
    self.path = user_directory + self.filename
    try:
      load_json(self.path)
    except Exception as e: 
      data = {"owner":self.owner_id, "words": {}}
      write_json(data, self.path)

  def open(self):
    return load_json(self.path)

  def update(self, data):
    write_json(data, self.path)
  
  def add_word(self, data):
    dictionary = load_json(self.path)
    dictionary['words'].update(data)
    write_json(dictionary, self.path)

  def del_word(self, index):
    l = []
    dictionary = load_json(self.path)
    for x,y in dictionary['words'].items():
        l.append(x)
    word = l[index]
    dictionary['words'].pop(word)
    self.update(dictionary)

  def show_all_words(self):
    words = ''
    j=0
    dictionary = load_json(self.path)
    for i in dictionary['words']: 
        word = str(j) + '. ' + i+' - '+ dictionary['words'][i] + "\n"
        words = words + word
        j+=1
    return words






