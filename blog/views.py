# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework import status, viewsets
# from rest_framework.response import Response
# from blog.models import Blog
# from blog.serializers import BlogSerializer
# from django.http import Http404
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
# from blog.permission import IsOwnerReadOnly

# class BlogList(APIView):
#     # Blog list를 보여줄 때
#     def get(self, request):
#         blogs = Blog.objects.all()
#         # 여러 개의 객체를 serialization하기 위해 many=True로 설정
#         serializer = BlogSerializer(blogs, many=True)
#         return Response(serializer.data)

#     # 새로운 Blog 글을 작성할 때
#     def post(self, request):
#         # request.data는 사용자의 입력 데이터
#         serializer = BlogSerializer(data=request.data)
#         if serializer.is_valid(): #유효성 검사
#             serializer.save() # 저장
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # Blog의 detail을 보여주는 역할
# class BlogDetail(APIView):
#     # Blog 객체 가져오기
#     def get_object(self, pk):
#         try:
#             return Blog.objects.get(pk=pk)
#         except Blog.DoesNotExist:
#             raise Http404

#     # Blog의 detail 보기
#     def get(self, request, pk, format=None):
#         blog = self.get_object(pk)
#         serializer = BlogSerializer(blog)
#         return Response(serializer.data)

#     # Blog 수정하기
#     def put(self, request, pk, format=None):
#         blog = self.get_object(pk)
#         serializer = BlogSerializer(blog, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     # Blog 삭제하기
#     def delete(self, request, pk, format=None):
#         blog = self.get_object(pk)
#         blog.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# # Blog의 목록, detail 보여주기, 수정하기, 삭제하기 모두 가능
# class BlogViewSet(viewsets.ModelViewSet):
#     # authentication 추가
#     authentication_classes = [BasicAuthentication, SessionAuthentication]
#     permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerReadOnly]
#     queryset = Blog.objects.all()
#     serializer_class = BlogSerializer

#     def perform_create(self, serializer):
#         serializer.save(user = self.request.user)
from .models import Blog
from .serializers import BlogSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from blog.permission import IsOwnerReadOnly
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
import logging
from config.hash import tolerantia
logger = logging.getLogger('my')
class BlogList(generics.ListCreateAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerReadOnly]
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        logger.info('Get', extra={'request':request})
        tolerantia()
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        logger.info('Post', extra={'request': request})
        tolerantia()
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class BlogDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerReadOnly]
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def retrieve(self, request, *args, **kwargs):
        # print(request)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        logger.info('Get', extra={'request':request})
        tolerantia()
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        logger.info('Put', extra={'request':request})
        tolerantia()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        serializer = self.get_serializer(instance)
        logger.info('Delete', extra={'request':request})
        tolerantia()
        return Response(status=status.HTTP_204_NO_CONTENT)
