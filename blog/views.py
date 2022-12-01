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
from .models import Blog, Comment
from .serializers import CommentSerializer, BlogCreateSerializer, BlogDetailSerializer, BlogListSerializer
from rest_framework import viewsets, generics, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from blog.permission import IsOwnerReadOnly
from rest_framework.response import Response

#log
import logging

# # Blog의 목록, detail 보여주기, 수정하기, 삭제하기 모두 가능
# class BlogViewSet(viewsets.ModelViewSet):
#     authentication_classes = [BasicAuthentication, SessionAuthentication]
#     permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerReadOnly]
#     queryset = Blog.objects.all()

#     logger = logging.getLogger('my')

#     serializer_class = BlogSerializer

# # serializer.save() 재정의
#     def perform_create(self, serializer):

#         self.logger.info(f'(blogview) : {self.request.user.id} : {self.request.blog.id}') # print log data to file
#         serializer.save(user = self.request.user)


class BlogCreate(generics.CreateAPIView):
    queryset            = Blog.objects.all()
    serializer_class    = BlogCreateSerializer
    permission_classes  = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = BlogCreateSerializer(data=request.data)

        if serializer.is_valid():
            blog = Blog.objects.create(
                    user_id    = request.user.id,
                    title      = request.data['title'],
                    content    = request.data['content'],
                    view_count = 0,
                    )
        
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BlogDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset            = Blog.objects.all()
    serializer_class    = BlogDetailSerializer
    permission_classes  = [IsAuthenticatedOrReadOnly]

class BlogList(generics.ListAPIView):
    queryset            = Blog.objects.all()
    serializer_class    = BlogListSerializer
    permission_classes  = [AllowAny]

class CommentCreate(generics.CreateAPIView):
    queryset            = Comment.objects.all()
    serializer_class    = CommentSerializer
    permission_classes  = [IsAuthenticatedOrReadOnly]

    def post(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            comment = Comment.objects.create(
                        user_id = request.user.id,
                        post_id = self.kwargs['pk'],
                        content = request.data['content']
                    )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset            = Comment.objects.all()
    serializer_class    = CommentSerializer
    permission_classes  = [IsAuthenticatedOrReadOnly]