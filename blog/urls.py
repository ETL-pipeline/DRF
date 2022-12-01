# from django.urls import path, include
# from .views import BlogViewSet
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('blog', BlogViewSet)

# urlpatterns =[
#     path('', include(router.urls))
# ]
from django.urls import path
from django.utils.functional import unpickle_lazyobject
from .views import CommentCreate, CommentDetail, BlogCreate, BlogDetail, BlogList
#from .views import BlogViewSet

# # Blog 목록 보여주기
# blog_list = BlogViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })

# # Blog detail 보여주기 + 수정 + 삭제
# blog_detail = BlogViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'delete': 'destroy'
# })
app_name = 'blog'
urlpatterns = [
        path('create', BlogCreate.as_view(), name='blog-create'),
        path('<int:pk>', BlogDetail.as_view(), name='blog-detail'),
        path('<int:pk>/comments', CommentDetail.as_view(), name='blog-comment'),
        path('<int:pk>/comments/create', CommentCreate.as_view(), name='blog-comment-create'),
        path('', BlogList.as_view(), name='blog-list'),
        ]
