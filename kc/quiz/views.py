from django.shortcuts import render
from .models import Team, Player

# Create your views here.
def verifyTeam(team_name,team_password):
    try:
        team = Team.objects.get(name=team_name)
        if team.password==team_password:
            return 2
        else:
            return 1
    except ObjectDoesNotExist:
        return 0
    
    
@permission_classes([AllowAny, ])
class createPlayer(generics.GenericAPIView):
    serializer_class = PlayerSerializer

    def post(self, request, *args, **kwargs):
        team_name=request.data['team_name']
        team_password=request.data['team_password']
        temp = verifyTeam(team_name,team_password)
        
        