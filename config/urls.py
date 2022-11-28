from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from user.views import RegisterAPIView, AuthAPIView, BlogList, BlogDetail
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", RegisterAPIView.as_view()), # post - 회원가입
    path("auth/", AuthAPIView.as_view()), # post - 로그인, delete - 로그아웃, get - 유저정보
    path("auth/refresh/", TokenRefreshView.as_view()), # jwt토큰 재발급
    path('blog/', BlogList.as_view()),
    path('blog/<int:pk>/', BlogDetail.as_view()),
    path('api-auth/', include('rest_framework.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)