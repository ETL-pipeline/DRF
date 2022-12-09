import requests
import random

def create_id(num):
    for i in range(1, num+1):
        bot = {
            "email":f"Bot{i}@bot.com",
            "password":"1111",
            "password2":"1111",
            "name":f"bot{i}",
            "login_id":f"bot{i}",
            "gender":random.choice(['M','F']),
            "phone_number":f"010{random.randint(10000000,99999999)}",
            "age":random.randint(1,100)
        }
        response = requests.post("http://127.0.0.1:8000/user/signup/", json=bot)
    return '성공'

if __name__ == '__main__':
    create_id(10)