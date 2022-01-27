from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Team


def remove(temp):
    p = temp.replace(" ", "")
    n = Team.objects.all().count()
    p = p + "_" + str(n)
    return p


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("password",)


class TeamRegisterSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Team
        fields = (
            "user",
            "team_name",
            "participant1",
            "participant1_email",
            "participant1_dc",
            "participant1_phone",
            "participant2",
            "participant2_email",
            "participant2_dc",
            "participant2_phone",
            "participant3",
            "participant3_email",
            "participant3_dc",
            "participant3_phone",
            "participant4",
            "participant4_email",
            "participant4_dc",
            "participant4_phone",
        )

    def create(self, data):
        temp = remove(data["team_name"])
        print(temp)
        user = User.objects.create_user(
            username=temp, password=data["user"]["password"]
        )
        team = Team(
            user=user,
            team_name=data["team_name"],
            participant1=data["participant1"],
            participant1_email=data["participant1_email"],
            participant1_dc=data["participant1_dc"],
            participant1_phone=data["participant1_phone"],
            participant2=data["participant2"],
            participant2_email=data["participant2_email"],
            participant2_dc=data["participant2_dc"],
            participant2_phone=data["participant2_phone"],
            participant3=data["participant3"],
            participant3_email=data["participant3_email"],
            participant3_dc=data["participant3_dc"],
            participant3_phone=data["participant3_phone"],
            participant4=data["participant4"],
            participant4_email=data["participant4_email"],
            participant4_dc=data["participant4_dc"],
            participant4_phone=data["participant4_phone"],
        )
        team.save()
        return user


class TeamNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ("team_name",)


class LoginSerializer(serializers.ModelSerializer):
    team = TeamNameSerializer()

    class Meta:
        model = User
        fields = ("team", "password")
