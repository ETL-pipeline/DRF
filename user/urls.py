from django.urls import path,include
from .views import RegisterAPIView, AuthAPIView
from rest_framework_simplejwt.views import TokenRefreshView # 토큰재발급받기
from rest_framework import urls
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('list', UserViewSet) #유저리스트 (테스트용)


urlpatterns = [
    path("register/", RegisterAPIView.as_view()), # post - 회원가입
    path("auth/", AuthAPIView.as_view()),  # post - 로그인, delete - 로그아웃, get - 유저정보
    path("auth/refresh/", TokenRefreshView.as_view()), # jwt토큰 재발급
    path("", include(router.urls)),   # 테스트용 viewset용으로 만든거 (용도?)
]