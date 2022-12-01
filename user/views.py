# from django.shortcuts import render
# from django.contrib.auth.models import User

# #DRF1

# import jwt
# from rest_framework.views import APIView
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
# from rest_framework import status, viewsets
# from rest_framework.permissions import IsAuthenticated
# from .serializers import *
# from rest_framework.response import Response
# from django.contrib.auth import authenticate, get_user_model
# from django.shortcuts import render, get_object_or_404
# from config.settings import SECRET_KEY
# from .serializers import UserSerializer, RegisterSerializer

# User = get_user_model()

# '''
# 회원가입 - jwt token auth
# '''
# class RegisterAPIView(APIView):
#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
            
#             # jwt 토큰 접근
#             token = TokenObtainPairSerializer.get_token(user)
#             refresh_token = str(token)
#             access_token = str(token.access_token)
#             res = Response(
#                 {
#                     "user": serializer.data,
#                     "message": "register successs",
#                     "token": {
#                         "access": access_token,
#                         "refresh": refresh_token,
#                     },
#                 },
#                 status=status.HTTP_200_OK,
#             )
            
#             # jwt 토큰 => 쿠키에 저장
#             res.set_cookie("access", access_token, httponly=True)
#             res.set_cookie("refresh", refresh_token, httponly=True)
            
#             return res
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# '''
# 유저 인증 - 로그인/로그아웃 - jwt token
# '''
# class AuthAPIView(APIView):
#     # 유저 정보 확인
#     def get(self, request):
#         try:
#             # access token을 decode 해서 유저 id 추출 => 유저 식별
#             access = request.COOKIES['access']
#             payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
#             pk = payload.get('user_id')
#             user = get_object_or_404(User, pk=pk)
#             serializer = RegisterSerializer(instance=user)
#             return Response(serializer.data, status=status.HTTP_200_OK)

#         except(jwt.exceptions.ExpiredSignatureError):
#             # 토큰 만료 시 토큰 갱신
#             data = {'refresh': request.COOKIES.get('refresh', None)}
#             serializer = TokenRefreshSerializer(data=data)
#             if serializer.is_valid(raise_exception=True):
#                 access = serializer.data.get('access', None)
#                 refresh = serializer.data.get('refresh', None)
#                 payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
#                 pk = payload.get('user_id')
#                 user = get_object_or_404(User, pk=pk)
#                 serializer = RegisterSerializer(instance=user)
#                 res = Response(serializer.data, status=status.HTTP_200_OK)
#                 res.set_cookie('access', access)
#                 res.set_cookie('refresh', refresh)
#                 return res
#             raise jwt.exceptions.InvalidTokenError

#         except(jwt.exceptions.InvalidTokenError):
#             # 사용 불가능한 토큰일 때
#             return Response(status=status.HTTP_400_BAD_REQUEST)

#     # 로그인
#     def post(self, request):
#         # 유저 인증
#         user = authenticate(
#             email=request.data.get("email"), password=request.data.get("password")
#         )
#         # 이미 회원가입 된 유저일 때
#         if user is not None:
#             serializer = RegisterSerializer(user)
#             # jwt 토큰 접근
#             token = TokenObtainPairSerializer.get_token(user)
#             refresh_token = str(token)
#             access_token = str(token.access_token)
#             res = Response(
#                 {
#                     "user": serializer.data,
#                     "message": "login success",
#                     "token": {
#                         "access": access_token,
#                         "refresh": refresh_token,
#                     },
#                 },
#                 status=status.HTTP_200_OK,
#             )
#             # jwt 토큰 => 쿠키에 저장
#             res.set_cookie("access", access_token, httponly=True)
#             res.set_cookie("refresh", refresh_token, httponly=True)
#             return res
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

#     # 로그아웃
#     def delete(self, request):
#         # 쿠키에 저장된 토큰 삭제 => 로그아웃 처리
#         response = Response({
#             "message": "Logout success"
#             }, status=status.HTTP_202_ACCEPTED)
#         response.delete_cookie("access")
#         response.delete_cookie("refresh")
#         return response

# jwt 토근 인증 확인용 뷰셋
# Header - Authorization : Bearer <발급받은토큰>

# class UserViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# 회원가입
from .models import User
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from user.serializers import SignupSirializer, SigninSirializer, UserSerializer
from rest_framework_tracking.mixins import LoggingMixin
class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSirializer
class SigninView(generics.GenericAPIView):
    serializer_class = SigninSirializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception = True)
        token = serializer.validated_data
        return Response({"token":token}, status=status.HTTP_200_OK)
class WithdrawalView(generics.DestroyAPIView):
    """ 회원탈퇴 뷰 - 요청을 보낸 사용자를 삭제합니다. """
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

#logging

class LoggingView(LoggingMixin, generics.GenericAPIView):
    def get(self, request):
        return Response('with logging')
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
