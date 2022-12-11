# 회원가입
from .models import User
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from user.serializers import SignupSirializer, SigninSirializer, UserSerializer
class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSirializer
class SigninView(generics.GenericAPIView):
    serializer_class = SigninSirializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True) # is_valid에서 체크에서 에러가 날 때, ValidationError를 raise
        token = serializer.validated_data
        refresh_token = token['refresh_token']
        access_token = token['access_token']
        res = Response(
            {
                "user": token['user'],
                "token": {
                    "refresh": refresh_token,
                    "access": access_token,
                },
            },
            status=status.HTTP_200_OK,
        )
        # 쿠키데이터 저장
        res.set_cookie("access", access_token, httponly=True)
        res.set_cookie("refresh", refresh_token, httponly=True)
        return res
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer