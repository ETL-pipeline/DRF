from django.urls import path
from user.views import SignupView, SigninView, UserViewSet

User_list = UserViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

User_detail = UserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

urlpatterns = [
    path("signup/", SignupView.as_view()),
    path('signin/', SigninView.as_view()),
    path('', User_list),
    path('<int:pk>', User_detail)
]