from django.urls import path, include
from .views import *

urlpatterns = [
    path('register', createPlayer.as_view(), name="registerTeam"),
]