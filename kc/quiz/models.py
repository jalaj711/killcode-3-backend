from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=500,primary_key=True)
    password = models.CharField(max_length=200)
    score = models.IntegerField(default=0)
    roundNo = models.IntegerField(default=1)

    def ___str___(self):
        return self.Team_Name

    


class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.cascade)
    name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(max_length=254)
    roll = models.CharField(max_length=200)
    
    def ___str___(self):
        return self.name+"("+self.team.name+")"

