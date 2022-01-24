from django.urls import path, include
from .views import *

urlpatterns = [
    path('register', register.as_view(), name="registerTeam"),
    path('login', login.as_view(), name="login"),
]