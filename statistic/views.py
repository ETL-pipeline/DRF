from django.shortcuts import render
from rest_framework.views import APIView
from user.models import User
from blog.models import Blog
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta
from django.utils import timezone

class UserGenderStatisticsView(APIView):
    def get(self, request):
        male_cnt = User.objects.filter(gender="M").count()
        female_cnt = User.objects.filter(gender="F").count()
        return Response({"male_count": male_cnt, "female_count": female_cnt}, status=status.HTTP_200_OK)

class BlogGenderStatisticsView(APIView):
    def get(self, request):
        male_cnt = Blog.objects.filter(user__gender="M").count()
        female_cnt = Blog.objects.filter(user__gender="F").count()
        return Response({"male_count": male_cnt, "female_count": female_cnt}, status=status.HTTP_200_OK)

class UserAgeStatisticsView(APIView):
    def get(self, request):
        children = User.objects.filter(age__range=(0,9)).count()
        teenager = User.objects.filter(age__range=(10,19)).count()
        in_ones_twenties = User.objects.filter(age__range=(20,29)).count()
        in_ones_thirties = User.objects.filter(age__range=(30,39)).count()
        in_ones_forites = User.objects.filter(age__range=(40,49)).count()
        in_ones_fifties = User.objects.filter(age__range=(50,59)).count()
        in_ones_sixties = User.objects.filter(age__range=(60,69)).count()
        old_senier = User.objects.filter(age__range=(70,99)).count()
        return Response({
            "children" : children,
            "teenager" : teenager,
            "in_ones_twenties" : in_ones_twenties,
            "in_ones_thirties" : in_ones_thirties,
            "in_ones_forites" : in_ones_forites,
            "in_ones_fifties" : in_ones_fifties,
            "in_ones_sixties" : in_ones_sixties,
            "old_senier" : old_senier,
        })

class ByTimeOfUserCountView(APIView):
    def get(self, response):
        recent = timezone.now() - timedelta(hours=24)
        common_1 = timezone.now() - timedelta(days=1)
        common_7 = timezone.now() - timedelta(days=7)
        # inf = datetime.date.today() - datetime.timedelta(years=100)
        recent_member = User.objects.filter(created_at__gte = recent).count()
        members  = User.objects.filter(created_at__range = (common_1, common_7)).count()
        VIP = User.objects.filter(created_at__lte = common_7).count()
        return Response({
            "recent_member" : recent_member,
            "Members" : members,
            "VIP" : VIP,
        })