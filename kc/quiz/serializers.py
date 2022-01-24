from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Team, Player


class TeamSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()
    # user_name = serializers.CharField()
    # user_email = serializers.EmailField()
    # user_roll = serializers.CharField()
    score = serializers.IntegerField(default=0)
    roundNo = serializers.IntegerField(default=1)

    class Meta:
        model = User
        fields = "__all__"

    def create(self, data):
        team = User.objects.create_user(
            username=data["username"], password=data["password"]
        )
        return team


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = "__all__"
