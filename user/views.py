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
        
        serializer.is_valid(raise_exception = True)
        token = serializer.validated_data
        return Response({"token":token}, status=status.HTTP_200_OK)
#logging
from rest_framework import generics
from rest_framework_tracking.mixins import LoggingMixin
class LoggingView(LoggingMixin, generics.GenericAPIView):
    def get(self, request):
        return Response('with logging')
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer