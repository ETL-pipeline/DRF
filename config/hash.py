import hashlib, base64
from b64uuid import B64UUID
from cryptography.fernet import Fernet
#from .settings import env
import json, math, gzip
from dateutil import parser
# https://ddolcat.tistory.com/713
from pathlib import Path
import os
import pymysql
import environ


BASE_DIR = Path(__file__).resolve().parent.parent
# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, "static") 

env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env(env_file=os.path.join(BASE_DIR, '.env'))
ENCRYPT_KEY = env('ENCRYPT_KEY')
SALT = env('SALT')
# def hashing_userid(id):
#     return hashlib.sha256((f"{id}").encode('ascii')).hexdigest()
# 한글은 암호화 지원이 안됨
# SyntaxError : bytes can only contain ASCII literal characters. 뜸
# > 아스키 문자만 지원
def hashing_userid(id):

    # 한글은 암호화 지원이 안됨
    # SyntaxError : bytes can only contain ASCII literal characters. 뜸
    # > 아스키 문자만 지원
    return hashlib.sha256(f"{id}".encode('ascii')).hexdigest()
        

class HashDjango:
    def __init__(self, key='keydata'):
        self.key = key
        self.data = None
        self.fernet = Fernet(self.gen_fernet_key(key))

          
    def encrypt_data(self, data):
        # 6개월에서 1년에 한 번씩 변경
        # key = Fernet.generate_key()
        #  >> 메서드를 호출할때 마다 새로운 키값 계속 형성
        i=1
        encrypt_str = self.fernet.encrypt(f"{data}".encode('ascii'))
        # print(encrypt_str)
        return encrypt_str

    def decrypt_data(self, encrypted_str):
        key = ENCRYPT_KEY.encode('ascii')
        fernet = Fernet(key)
        decrypt_str = fernet.decrypt(encrypted_str)
        # print(decrypt_str)
        return decrypt_str

    def gen_fernet_key(self, passcode:bytes) -> bytes:

        assert isinstance(passcode, bytes)

        hlib = hashlib.md5()
        hlib.update(passcode)

        return base64.urlsafe_b64encode(hlib.hexdigest().encode('ascii'))

HD = HashDjango(bytes(ENCRYPT_KEY, 'utf-8'))

def tolerantia():
    with open('logs/mysite.log','r') as f:
        line = f.readlines()[-1]
    
    data = json.loads(line)
    # print(type(data))
    # print(data)
    # print(data['detail'])
    
    time = data['inDate']
    epoch_time = parser.parse(time).timestamp()

    temp = dict()
    temp['recordid'] = data['user_id']
    temp['timestamp'] = math.trunc(epoch_time)
    #enc = HD.encrypt_data(data['detail'])
    #print(gzip.compress(enc))
    #temp['data'] = gzip.compress(enc).decode('utf-8')
    temp['data'] = HD.encrypt_data(data['detail']).decode('utf-8')

    json_ = json.dumps(temp, indent=4)+',\n'

    with open('logs/logInfo.json','a') as f:
        f.write(json_)