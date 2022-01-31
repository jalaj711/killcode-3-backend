from django.urls import path, include
from knox.views import LogoutView
from .views import *

urlpatterns = [
    path("register", register.as_view(), name="registerTeam"),
    path("login", login.as_view(), name="login"),
    path("round", round.as_view(), name="round"),
    path("profiles", profiles.as_view(), name="profile"),
    path("evidence", evidence.as_view(), name="evidence"),
    path("storeAnswer", storeAnswer.as_view(), name="storeAnswer"),
    path("killcode", killcode.as_view(), name="killcode"),
    path("leaderboard", leaderboard.as_view(), name="leaderboard"),
    path("saveParticipants", Teams, name="download_p"),
    path("saveLeaderboard", Leaderboard, name="download_l"),
]
