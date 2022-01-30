from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.utils import timezone


class Team(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=200, primary_key=True)
    participant1 = models.CharField(max_length=200, blank=True)
    participant1_email = models.EmailField(max_length=254, blank=True)
    participant1_dc = models.CharField(max_length=100, blank=True)
    participant1_phone = models.CharField(max_length=20, blank=True)
    participant2 = models.CharField(max_length=200, blank=True)
    participant2_email = models.EmailField(max_length=254, blank=True)
    participant2_dc = models.CharField(max_length=100, blank=True)
    participant2_phone = models.CharField(max_length=20, blank=True)
    participant3 = models.CharField(max_length=200, blank=True)
    participant3_email = models.EmailField(max_length=254, blank=True)
    participant3_dc = models.CharField(max_length=100, blank=True)
    participant3_phone = models.CharField(max_length=20, blank=True)
    participant4 = models.CharField(max_length=200, blank=True)
    participant4_email = models.EmailField(max_length=254, blank=True)
    participant4_dc = models.CharField(max_length=100, blank=True)
    participant4_phone = models.CharField(max_length=20, blank=True)
    score = models.IntegerField(default=0)
    penalty = models.IntegerField(default=0)
    final_score = models.IntegerField(default=0)
    guessed = models.BooleanField(default=0)
    rank = models.IntegerField(default=0)
    submit_time = models.DateTimeField(default=datetime.now)

    def ___str___(self):
        return self.team_name


class Killcode(models.Model):
    team = models.OneToOneField(Team, on_delete=models.CASCADE)
    answer = models.CharField(max_length=200)

    def ___str___(self):
        return self.team.team_name


class Profile(models.Model):
    name = models.CharField(max_length=400)
    data = models.TextField()
    image = models.ImageField(upload_to="profilepics/", blank=True, default=None)

    def ___str___(self):
        return self.name


class Round(models.Model):
    round_no = models.IntegerField(default=1)
    riddle = models.TextField()
    killer_msg = models.TextField()
    ca = models.TextField(default=None)
    ca_location = models.CharField(max_length=400)
    ca_victim = models.CharField(max_length=400)
    tries = models.IntegerField(default=3)
    start_time = models.DateTimeField(default=datetime.now)
    end_time = models.DateTimeField(default=datetime.now)

    def ___str___(self):
        return self.round_no


class Evidence(models.Model):
    round = models.OneToOneField(Round, on_delete=models.CASCADE)
    text = models.TextField(default=None)
    image = models.ImageField(blank=True, upload_to="evidenceImage/", default=None)

    def ___str___(self):
        return self.round.round_no


class Answer(models.Model):
    team = models.OneToOneField(Team, on_delete=models.CASCADE)
    round = models.OneToOneField(Round, on_delete=models.CASCADE)
    location = models.CharField(max_length=400)
    victim = models.CharField(max_length=400)
    submit_time = models.DateTimeField(auto_now=True)
    tries = models.IntegerField(default=1)

    def ___str___(self):
        return self.round.round_no + "_" + self.team.team_name


class Notification(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    notification = models.TextField()

    def ___str___(self):
        return self.round.round_no


class Universal(models.Model):
    start_time = models.DateTimeField(default=datetime.now)
    end_time = models.DateTimeField(default=datetime.now)
    leaderboard_freeze = models.BooleanField(default=0)
    killcode = models.CharField(max_length=200)

    def __str__(self):
        return "Duration"
