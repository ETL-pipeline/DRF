import requests, json, random

def select_id(num):
    bot_info = []
    for _ in range(num):
        bot = {
            'login_id':f"bot{random.randint(1,10)}",
            'password':"1111"
        }
        bot_info.append(bot)
    return bot_info

def get_accessKey(bot_info):
    accessKey = []
    for bot in bot_info:
        response = requests.post('http://127.0.0.1:8000/user/signin/', json=bot)
        json_ = json.loads(response.text)
        accessKey.append(json_['token']['access'])
    return accessKey

def create_post(accessKey):
    for key in accessKey:
        idx = random.randint(1, 101)
        header = {'Authorization':f"Bearer {key}"}
        data = {
            'title':f'Bot {idx}',
            'body':f'아무거나 적어놓는 {idx} 뭔가를 적어놔야하는데 뭘적을까ㅣ요'
        }
        response = requests.post('http://127.0.0.1:8000/blog/', json=data, headers=header)
        text = json.loads(response.text)

def bot_schedule(num):
    bots = select_id(num)
    accesskey = get_accessKey(bots)
    create_post(accesskey)