from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from user.models import User



class TestUser(APITestCase):
    '''
        users app의 API 3개(회원가입, 로그인, 회원탈퇴) unit test
    '''
    def setUp(self):
        self.user = User(
            id       = 1,
            login_id = "codestates",
            password = make_password("123"),
            name     = "aaa",
            email    = "aaa@gmail.com",
            phone_number = "01012345678",
            age = 20,
            gender = "M",
            
        )
        self.user.save()
        

    # 회원가입
    def test_register_success(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        
        self.user_data = {
            "login_id"      : "codestates1",
            "password"      : "111222333",
            "password2"     : "111222333",
            "name"          : "홍길동",
            "email"         : "abc@gmail.com",
            "phone_number"  : "01011111111",
            "age"           : "20",
            "gender"        : "M",
            }

        self.register_url = "/user/signup/"
        self.response = self.client.post(self.register_url, data = self.user_data, format='json')
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    # 회원가입 중복아이디 체크 실패
    def test_register_id_ckeck_fail(self):
        
        self.user_data = {
            "login_id"      : "codestates", # 중복아이디
            "password"      : "111222333",
            "password2"     : "111222333",
            "name"          : "홍길동",
            "email"         : "abc@gmail.com",
            "phone_number"  : "01011111111",
            "age"           : "20",
            "gender"        : "M",
            }

        self.register_url = "/user/signup/"
        self.response = self.client.post(self.register_url, data = self.user_data, format='json')
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

    #회원가입 중복핸드폰번호 체크 실패
    def test_register_phonenumber_ckeck_fail(self):
        
        self.user_data = {
            "login_id"      : "codestates2", #
            "password"      : "111222333",
            "password2"     : "111222333",
            "name"          : "홍길동",
            "email"         : "abc@gmail.com",
            "phone_number"  : "01012345678",# 중복 핸드폰번호
            "age"           : "20",
            "gender"        : "M",  
            }

        self.register_url = "/user/signup/"
        self.response = self.client.post(self.register_url, data = self.user_data, format='json')
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

    # 회원가입시 패스워드 확인 실패
    def test_register_password_check_fail(self):
        
        self.user_data = {
            "login_id"      : "codestates112",
            "password"      : "111222333",
            "password2"     : "111111111", # 패스워드 확인 오류
            "name"          : "홍길동",
            "email"         : "abc@gmail.com",
            "phone_number"  : "01011111111",
            "age"           : "20",
            "gender"        : "M",
            }

        self.register_url = "/user/signup/"
        self.response = self.client.post(self.register_url, data = self.user_data, format='json')
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

    # 로그인
    def test_login_success(self):
        self.login_url = "/user/signin/"
        data= {
                "login_id": "codestates",
                "password": "123",
            }
        response= self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # 비밀번호 불일치
    def test_password_fail(self):
        self.login_url = "/user/signin/"
        data= {
                "login_id": "codestates",
                "password": "133",
            }
        response= self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {'login_id': "{'detail': 'No active account found with the given credentials'}"})

    # 회원탈퇴
    def test_withdraw_success(self):
        self.withdraw_url = f"/user/{self.user.id}/withdraw/"

        client = APIClient()
        client.force_authenticate(user=self.user)

        response = client.delete(self.withdraw_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)