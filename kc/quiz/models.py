from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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

    def ___str___(self):
        return self.user.username
