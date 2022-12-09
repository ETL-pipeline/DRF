from django.urls import path
from blog.views import BlogList, BlogDetail, BlogCreate
from blog.serializers import BlogSerializer
from blog.models import Blog
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns =[
    path('', BlogList.as_view(queryset=Blog.objects.all(), serializer_class=BlogSerializer)),
    path('<int:pk>/', BlogDetail.as_view(queryset=Blog.objects.all(), serializer_class=BlogSerializer)),
    path('create/', BlogCreate.as_view()),
]