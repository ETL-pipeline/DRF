from cryptography.fernet import Fernet
from .settings import env
import json, os, time, gzip, math, hashlib, base64
from dateutil import parser
from datetime import datetime
from b64uuid import B64UUID
from config import s3uploading
# https://ddolcat.tistory.com/713

ENCRYPT_KEY = env('ENCRYPT_KEY')
SALT = env('SALT')
S3 = s3uploading.S3instant()

def hashing_userid(id):
    return hashlib.sha256((f"{id}").encode('ascii')).hexdigest()
# 한글은 암호화 지원이 안됨
# SyntaxError : bytes can only contain ASCII literal characters. 뜸
# > 아스키 문자만 지원
class HashDjango():
    def __init__(self, key='keydata'):
        self.key = key
        self.data = None
        self.fernet = Fernet(self.gen_fernet_key(key))

    def encrypt_data(self, data):
        # 6개월에서 1년에 한 번씩 변경
        # key = Fernet.generate_key()
        #  >> 메서드를 호출할때 마다 새로운 키값 계속 형성
        encrypt_str = self.fernet.encrypt(f"{data}".encode('ascii'))
        return encrypt_str

    def decrypt_data(self, encrypted_str):
        key = ENCRYPT_KEY.encode('ascii')
        fernet = Fernet(key)
        decrypt_str = fernet.decrypt(encrypted_str)
        return decrypt_str

    def gen_fernet_key(self, passcode:bytes) -> bytes:

        assert isinstance(passcode, bytes)

        hlib = hashlib.md5()
        hlib.update(passcode)

        return base64.urlsafe_b64encode(hlib.hexdigest().encode('ascii'))

HD = HashDjango(bytes(ENCRYPT_KEY, 'utf-8'))

def tolerantia():
    with open('logs/mysite.log','r') as f:
        line = f.readlines()
    
    data = json.loads(line[-1])
    indate = data['inDate']
    epoch_time = time.mktime(datetime.strptime(indate, '%y%m%d%H%M%S%f').timetuple())
    temp = dict()
    temp['recordid'] = data['user_id']
    temp['timestamp'] = math.trunc(epoch_time)
    temp['data'] = HD.encrypt_data(data['detail']).decode('utf-8')

    json_ = json.dumps(temp, indent=4)+',\n'

    # with gzip.open('logs/logInfo.json.gz','a') as f:
    #     f.write(json_)
    if len(line) > 20:
        with gzip.open('logs/logInfo.json.gz', 'wb') as f:
            f.write(json_.encode('utf-8'))
        with open('logs/mysite.log','w') as f:
            f.write('')
            
        S3.s3uploadlog('logs/logInfo.json.gz')


