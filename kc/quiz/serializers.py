from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Team


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password")


class TeamRegisterSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Team
        fields = (
            "user",
            "participant1",
            "participant1_email",
            "participant2",
            "participant2_email",
            "participant3",
            "participant3_email",
            "participant4",
            "participant4_email",
        )

    def create(self, data):
        user = User.objects.create_user(
            username=data["user"]["username"], password=data["user"]["password"]
        )
        team = Team(
            user=user,
            participant1=data["participant1"],
            participant1_email=data["participant1_email"],
            participant2=data["participant2"],
            participant2_email=data["participant2_email"],
            participant3=data["participant3"],
            participant3_email=data["participant3_email"],
            participant4=data["participant4"],
            participant4_email=data["participant4_email"],
        )
        team.save()
        return user
    
    
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password")
