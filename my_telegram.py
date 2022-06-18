import requests


class BOT():
    def __init__(self, token):
        self.token = token
        self.URL = 'https://api.telegram.org/bot{token}/'.format(
            token=self.token)
        self.updates = []
        self.update_id = 0
        self.text = None
        self.offset = False

    def get_updates(self):
        url = self.URL + "getUpdates"
        if self.offset:
            r = requests.get(url, params={'offset': self.update_id})
            self.offset = False
        else:
            r = requests.get(url)
            d = r.json()
            if len(d['result']) > 10:
                self.offset = True
        self.updates = r.json()
        try:
            self.text = self.updates['result'][-1]['message']['text']
        except:
            pass

        
    def is_new_updates(self):
        self.get_updates()
        if len(self.updates['result']) == 0:
            return False
        elif self.updates['result'][-1]['update_id'] == self.update_id:
            return False
        elif self.updates['result'][-1]['update_id'] != self.update_id:
            self.update_id = self.updates['result'][-1]['update_id']
            return True

    def send_message(self, user, **kwargs):
        url = self.URL + 'sendMessage'
        answer = {'chat_id': user.chat_id }
        for x,y in kwargs.items():
            answer[x] = y
        r = requests.post(url, json = answer)


