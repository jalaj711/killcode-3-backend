from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    participant1 = models.CharField(max_length=200, blank=True)
    participant1_email = models.EmailField(max_length=254, blank=True)
    participant2 = models.CharField(max_length=200, blank=True)
    participant2_email = models.EmailField(max_length=254, blank=True)
    participant3 = models.CharField(max_length=200, blank=True)
    participant3_email = models.EmailField(max_length=254, blank=True)
    participant4 = models.CharField(max_length=200, blank=True)
    participant4_email = models.EmailField(max_length=254, blank=True)
    participant5 = models.CharField(max_length=200, blank=True)
    participant5_email = models.EmailField(max_length=254, blank=True)

    def ___str___(self):
        return self.user.username
