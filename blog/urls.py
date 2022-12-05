from django.urls import path
from blog.views import BlogList, BlogDetail
from blog.serializers import BlogSerializer
from blog.models import Blog
from rest_framework.urlpatterns import format_suffix_patterns
# from .views import BlogViewSet
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
urlpatterns =[
    path('', BlogList.as_view(queryset=Blog.objects.all(), serializer_class=BlogSerializer)),
    path('<int:pk>/', BlogDetail.as_view(queryset=Blog.objects.all(), serializer_class=BlogSerializer)),
]