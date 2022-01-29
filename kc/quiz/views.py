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
from rest_framework import status
from django.contrib.auth import authenticate
from django.http import HttpResponse
import csv


def remove(temp):
    return temp.replace(" ", "")


@permission_classes(
    [
        AllowAny,
    ]
)
class register(generics.GenericAPIView):
    serializer_class = TeamRegisterSerializer

    def post(self, request, *args, **kwargs):
        if (
            request.data.get("participant1") != ""
            and request.data.get("participant2") != ""
        ):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            return Response(
                {
                    "token": AuthToken.objects.create(user)[1],
                    "status": 200,
                }
            )
        return Response(
            "Less than 2 participants not allowed.", status=status.HTTP_400_BAD_REQUEST
        )


@permission_classes(
    [
        AllowAny,
    ]
)
class login(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        team = Team.objects.filter(team_name=request.data.get("team")["team_name"])[0]
        user = authenticate(
            username=team.user.username, password=request.data.get("password")
        )
        if user is not None:
            return Response(
                {
                    "user": UserSerializer(
                        user, context=self.get_serializer_context()
                    ).data,
                    "token": AuthToken.objects.create(user)[1],
                    "status": 200,
                }
            )
        else:
            return Response(
                "Wrong Credentials! Please try again.", status=status.HTTP_403_FORBIDDEN
            )


class check(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        return Response(
            "Registered/Logged in successfully. User is authenticated.",
            status=status.HTTP_200_OK,
        )


def Teams(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="teams.csv"'
    writer = csv.writer(response)
    for team in Team.objects.all():
        writer.writerow(
            [
                team.team_name,
                team.participant1,
                team.participant1_email,
                team.participant1_dc,
                team.participant1_phone,
                team.participant2,
                team.participant2_email,
                team.participant2_dc,
                team.participant2_phone,
                team.participant3,
                team.participant3_email,
                team.participant3_dc,
                team.participant3_phone,
                team.participant4,
                team.participant4_email,
                team.participant4_dc,
                team.participant4_phone,
            ]
        )
    return response