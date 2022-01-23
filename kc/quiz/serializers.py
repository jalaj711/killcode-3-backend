from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Team, Player


class TeamSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    password = serializers.CharField()
    score = serializers.IntegerField()
    roundNo = serializers.IntegerField()

    class Meta:
        model = User
        fields = ('name', 'password', 'score', 'roundNo')

    def create(self, data):
        user = User.objects.create_user(username=data['username'],
        password=data['password']
        return user


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'