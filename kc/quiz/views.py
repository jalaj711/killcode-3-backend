from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from rest_framework import viewsets, generics, authentication, permissions
from knox.models import AuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes, APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import *
from .serializers import *

# Create your views here.
def verifyTeam(team_name, team_password):
    try:
        Team.objects.get(name=team_name)
        return 1
    except ObjectDoesNotExist:
        return 0


@permission_classes(
    [
        AllowAny,
    ]
)
class createPlayer(generics.GenericAPIView):
    serializer_class = TeamSerializer

    def post(self, request, *args, **kwargs):
        team_name = request.data.get("name")
        team_password = request.data.get("password")
        temp = verifyTeam(team_name, team_password)
        res = {
            "name": request.data.get("name"),
            "password": request.data.get("password"),
        }
        if temp == 0:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            team = serializer.save()
            # player = Player.objects.create(
            #     team=request.data.get("team_name"),
            #     name=request.data.get("user_name"),
            #     email=request.data.get("user_email"),
            #     roll=request.data.get("user_roll"),
            # )
            # print(player)
            print(serializer.data)
            return Response(
                {
                    "team": serializer.data,
                    # "player": player,
                    "token": AuthToken.objects.create(team)[1],
                    "status": 200,
                }
            )
        
        elif temp == 1:
            team = Team.objects.get(name=request.data.get("name"))
            return Response(
                {
                    "team": team,
                    "message": "team already exists",
                    "status": 400,
                }
            )
            