from django.urls import path, include
from knox.views import LogoutView
from .views import *

urlpatterns = [
    path('register', register.as_view(), name="registerTeam"),
    path('login', login.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('check', check.as_view(), name="check"),   
]