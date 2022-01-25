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
        return Response("Less than 2 participants not allowed.", status=status.HTTP_400_BAD_REQUEST)


@permission_classes(
    [
        AllowAny,
    ]
)
class login(generics.GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request, *args, **kwargs):
        user = authenticate(username=request.data.get("username"), password=request.data.get("password"))
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
            return Response("Wrong Credentials! Please try again.", status=status.HTTP_403_FORBIDDEN)
        
        
class check(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        return Response("Registered/Logged in successfully. User is authenticated.", status=status.HTTP_200_OK)