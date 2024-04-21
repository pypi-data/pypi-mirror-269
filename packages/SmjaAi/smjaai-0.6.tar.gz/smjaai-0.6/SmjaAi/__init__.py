import requests , random
class Ai:
    def __init__(self, text):
        self.text = text

    def GPT(self):
        while True:
            rq = '123'
            d = random.choice(rq)
            e = random.choice(rq)
            c = random.choice(rq)
            b = random.choice(rq)
            j = d + e
            url = 'https://backend.aichattings.com/api/v2/chatgpt/talk'
            data = {'ep_user_id': j+'62','locale':' en','model':' gpt3','msg':str(self.text)}
            req = requests.post(url,data=data).text
            da = {'text':req,
            'status':'successfully'}
            return da
       

