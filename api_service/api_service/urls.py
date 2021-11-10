# encoding: utf-8

from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api import views as api_views
from api import web_views

urlpatterns = [
    path('auth/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('stock', api_views.StockView.as_view(), name='stock'),
    path('history', api_views.HistoryView.as_view(), name='history'),
    path('stats', api_views.StatsView.as_view(), name='stats'),
    path('admin', admin.site.urls, name='admin'),
    path("register", web_views.register, name="register"),
    # Authentication pages
    path("login", web_views.login_user, name="login"),
    path("logout", web_views.logout, name="logout"),
    path("", web_views.home, name="home"),
]
