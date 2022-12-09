from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/refresh/", TokenRefreshView.as_view()), # jwt토큰 재발급
    path('api-auth/', include('rest_framework.urls')),
    path("blog/", include("blog.urls")),
    path("statistic/", include('statistic.urls')),
    path("user/", include('user.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
