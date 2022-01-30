from rest_framework import viewsets, generics, authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes, APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from knox.models import AuthToken
from rest_framework import status
from .models import *
from .serializers import *
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.utils import timezone
import csv


def remove(temp):
    return temp.replace(" ", "")


def check_duration():
    tm = timezone.now()
    obj = Universal.objects.all().first()
    if tm > obj.end_time:
        Universal.leaderboard_freeze = 1
    return


def check_round():
    tm = timezone.now()
    rounds = Round.objects.all()
    for round in rounds:
        if tm > round.start_time and tm <= round.end_time:
            return round.round_no
        else:
            return -1


def latest_round():
    tm = timezone.now()
    rounds = Round.objects.all()
    max = 0
    for round in rounds:
        if tm > round.end_time:
            if round.round_no > max:
                max = round.round_no
    return max


def check_ans(a, b):
    a = a.lower().strip().replace(" ", "")
    b = b.lower().strip().replace(" ", "")
    if a == b:
        return True
    return False


def calculate_penalty(username):
    round_no = latest_round()
    team = Team.objects.filter(user__username=username)
    if round_no <= 5:
        team.penalty += (round_no) * 5
    else:
        team.score += (2 * round.round_no - 5) * 5


def calculate():
    round_no = max(latest_round(), check_round())
    round = Round.objects.get(round_no=round_no)
    teams = Team.objects.all()
    for team in teams:
        answer = Answer.objects.filter(round=round, team=team).first()
        if answer is not None:
            if round_no <= 5:
                if check_ans(answer.location, round.ca_location):
                    team.score += (round.round_no) * 5
                if check_ans(answer.victim, round.ca_victim):
                    team.score += (round.round_no) * 5
            else:
                if check_ans(answer.location, round.ca_location):
                    team.score += (2 * round.round_no - 5) * 5
                if check_ans(answer.victim, round.ca_victim):
                    team.score += (2 * round.round_no - 5) * 5


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
        return Response(
            "Less than 2 participants not allowed.", status=status.HTTP_400_BAD_REQUEST
        )


@permission_classes(
    [
        AllowAny,
    ]
)
class login(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        team = Team.objects.filter(team_name=request.data.get("team")["team_name"])[0]
        user = authenticate(
            username=team.user.username, password=request.data.get("password")
        )
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
            return Response(
                "Wrong Credentials! Please try again.", status=status.HTTP_403_FORBIDDEN
            )


@permission_classes([IsAuthenticated])
class profiles(APIView):
    def get(self, request):
        profiles = Profile.objects.all()
        profiles_array = []
        for profile in profiles:
            profiles_array.append(
                {
                    "name": str(profile.name),
                    "data": str(profile.data),
                    "image": str(profile.image),
                }
            )
        return Response(profiles_array, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class round(APIView):
    def get(self, request):
        round_no = check_round()
        if round_no == -1:
            return Response(
                "No rounds live",
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            round = Round.objects.get(round_no=round_no)
            next_round = Round.objects.get(round_no=round_no + 1)
            if next_round is not None:
                return Response(
                    {
                        "round_no": round_no,
                        "riddle": round.riddle,
                        "killer_msg": round.killer_msg,
                        "next_round_start_time": next_round.start_time,
                        "next_round_end_time": next_round.end_time,
                        "status": 200,
                    }
                )
            else:
                return Response(
                    {
                        "round_no": round_no,
                        "riddle": round.riddle,
                        "killer_msg": round.killer_msg,
                        "next_round_start_time": "NULL",
                        "next_round_end_time": "NULL",
                        "status": 200,
                    }
                )


@permission_classes([IsAuthenticated])
class evidence(APIView):
    def get(self, request):
        round_no = latest_round()
        live_round = check_round()
        notifs = Notification.objects.filter(round__round_no=live_round)
        notif_array = []
        if notifs is not None:
            for notif in notifs:
                notif_array.append(
                    {
                        "notification": str(notif.notification),
                    }
                )
        evidence_array = []
        if round_no == 0:
            return Response(evidence_array, notif_array, status.HTTP_400_BAD_REQUEST)
        else:
            evidences = Evidence.objects.order_by("round__round_no")
            for evidence in evidences:
                if evidence.round.round_no <= round_no:
                    evidence_array.append(
                        {
                            "round": str(evidence.round.round_no),
                            "text": str(evidence.text),
                            "image": str(evidence.image),
                        }
                    )
            return Response(evidence_array, notif_array, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class storeAnswer(APIView):
    def post(self, request):
        round_no = check_round()
        if round_no == -1:
            return Response(
                "No rounds live.",
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            team = Team.objects.get(user__username=request.user.username)
            round = Round.objects.get(round_no=round_no)
            answer = Answer.objects.filter(team=team, round=round)
            n = answer.count()
            if n == 0:
                answer = Answer(
                    team=team,
                    round=round,
                    location=request.data.get("location"),
                    victim=request.data.get("victim"),
                )
                team.submit_time = answer.submit_time
                return Response("Answer saved successfully.", status=status.HTTP_200_OK)
            else:
                answer = answer[0]
                if answer.tries < round.tries:
                    answer.location = request.data.get("location")
                    answer.location = request.data.get("victim")
                    answer.tries += 1
                    answer.save()
                    team.submit_time = answer.submit_time
                    return Response(
                        "Answer saved successfully.", status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        "Number of tries are over.", status=status.HTTP_403_FORBIDDEN
                    )


@permission_classes([IsAuthenticated])
class killcode(APIView):
    def post(self, request):
        killcode = request.data.get("killcode")
        if check_ans(killcode, Universal.killcode):
            Universal.leaderboard_freeze = 1
        else:
            calculate_penalty(request.user.username)


@permission_classes([IsAuthenticated])
class leaderboard(APIView):
    def get(self, request, format=None):
        check_duration()
        if check_round() == -1 or Universal.leaderboard_freeze:
            calculate()
        teams_array = []
        current_rank = 1
        teams = Team.objects.order_by("-score", "submit_time")
        for team in teams:
            participant_array = []
            participant_array.append(
                {
                    "participant1": str(team.participant1),
                    "participant2": str(team.participant2),
                    "participant3": str(team.participant3),
                    "participant4": str(team.participant4),
                }
            )
            team.rank = current_rank
            teams_array.append(
                {
                    "name": str(team.team_name),
                    "participant_array": participant_array,
                    "score": str(team.final_score),
                    "rank": str(team.rank),
                }
            )
            current_rank += 1
        return Response(teams_array, status=status.HTTP_200_OK)


def Teams(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="teams.csv"'
    writer = csv.writer(response)
    for team in Team.objects.all():
        writer.writerow(
            [
                team.team_name,
                team.participant1,
                team.participant1_email,
                team.participant1_dc,
                team.participant1_phone,
                team.participant2,
                team.participant2_email,
                team.participant2_dc,
                team.participant2_phone,
                team.participant3,
                team.participant3_email,
                team.participant3_dc,
                team.participant3_phone,
                team.participant4,
                team.participant4_email,
                team.participant4_dc,
                team.participant4_phone,
            ]
        )
    return response
