from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from user.views import SignupView, SigninView
from rest_framework_simplejwt.views import TokenRefreshView
from blog.views import BlogViewSet

urlpatterns = [
    path("admin/", admin.site.urls),
    path("signup/", SignupView.as_view()), # post - 회원가입
    path("auth/refresh/", TokenRefreshView.as_view()), # jwt토큰 재발급
    path('api-auth/', include('rest_framework.urls')),
    path("", include("blog.urls")),
    path('signin/', SigninView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)