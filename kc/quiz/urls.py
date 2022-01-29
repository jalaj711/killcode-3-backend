from django.urls import path, include
from knox.views import LogoutView
from .views import *

urlpatterns = [
    path("register", register.as_view(), name="registerTeam"),
    path("login", login.as_view(), name="login"),
    path("round", round.as_view(), name="round"),
    path("profile", profile.as_view(), name="profile"),
    path("evidence", evidence.as_view(), name="evidence"),
    path("storeAnswer", storeAnswer.as_view(), name="storeAnswer"),
    path("leaderboard", leaderboard.as_view(), name="leaderboard"),
    path("check", check.as_view(), name="check"),
    path("saveParticipants", Teams, name="download"),
]
