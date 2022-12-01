# from django.urls import path, include
# from .views import BlogViewSet
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('blog', BlogViewSet)

# urlpatterns =[
#     path('', include(router.urls))
# ]
from django.urls import path
from .views import BlogViewSet

# Blog 목록 보여주기
blog_list = BlogViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

# Blog detail 보여주기 + 수정 + 삭제
blog_detail = BlogViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

urlpatterns =[
    path('', blog_list),
    path('<int:pk>/', blog_detail),
]
