import hashlib
from cryptography.fernet import Fernet
from .settings import env

# https://ddolcat.tistory.com/713

ENCRYPT_KEY = env('ENCRYPT_KEY')

def hashing_userid(id):
    return hashlib.sha256((f"{id}").encode('ascii')).hexdigest()
# 한글은 암호화 지원이 안됨
# SyntaxError : bytes can only contain ASCII literal characters. 뜸
# > 아스키 문자만 지원

def encrypt_data(data):
    # 6개월에서 1년에 한 번씩 변경
    # key = Fernet.generate_key()
    #  >> 메서드를 호출할때 마다 새로운 키값 계속 형성

    key = ENCRYPT_KEY.encode('ascii')
    fernet = Fernet(key)
    encrypt_str = fernet.encrypt(f"{data}".encode('ascii'))
    print(encrypt_str)
    return encrypt_str

def decrypt_data(encrypted_str):
    key = ENCRYPT_KEY.encode('ascii')
    fernet = Fernet(key)
    decrypt_str = fernet.decrypt(encrypted_str)
    print(decrypt_str)
    return decrypt_str