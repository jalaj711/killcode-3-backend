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


@permission_classes(
    [
        AllowAny,
    ]
)
class register(generics.GenericAPIView):
    serializer_class = TeamRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        team = serializer.save()
        return Response(
            {
                "token": AuthToken.objects.create(team)[1],
                "status": 200,
            }
        )


@permission_classes(
    [
        AllowAny,
    ]
)
class login(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        d = request.data.get("user")
        user = authenticate(username=d["username"], password=d["password"])
        if user is not None:
            return Response(
                {
                    "user": UserSerializer(
                        user, context=self.get_serializer_context()
                    ).data,
                    "token": AuthToken.objects.create(user)[1],
                }
            )
        else:
            return Response("Not Allowed", status=status.HTTP_403_FORBIDDEN)
