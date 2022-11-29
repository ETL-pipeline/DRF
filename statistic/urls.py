from django.urls import path
from statistic.views import BlogGenderStatisticsView, \
    UserGenderStatisticsView, UserAgeStatisticsView, ByTimeOfUserCountView

urlpatterns = [
    path('BlogGenderCount/', BlogGenderStatisticsView.as_view()),
    path('UserGenderCount/', UserGenderStatisticsView.as_view()),
    path('UserAgeCount/', UserAgeStatisticsView.as_view()),
    path('ByTimeOfUserCount/', ByTimeOfUserCountView.as_view()),
]