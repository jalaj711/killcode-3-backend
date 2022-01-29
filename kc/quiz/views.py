from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from rest_framework import viewsets, generics, authentication, permissions
from knox.models import AuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes, APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import *
from .serializers import *
from rest_framework import status
from django.contrib.auth import authenticate
from django.http import HttpResponse
import csv
from django.utils import timezone


def remove(temp):
    return temp.replace(" ", "")


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


def calculate():
    round_no = latest_round()
    round = Round.objects.get(round_no=round_no)
    answers = Answer.objects.filter(round=round).order_by("submit_time")
    for answer in answers:
        # answer = Answer.objects.filter(round=round, team=team)
        # print(answer)
        # answer = answer[0]
        if check_ans(answer.location, round.ca_location):
            answer.team.score += (round.round_no) * 5
        if check_ans(answer.victim, round.ca_victim):
            answer.team.score += (round.round_no) * 5


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
class profile(APIView):
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
        return Response(
            {
                "profiles": profiles_array,
                "status": 200,
            }
        )


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
            return Response(
                {
                    "riddle": round.riddle,
                    "killer_msg": round.killer_msg,
                    "status": 200,
                }
            )


@permission_classes([IsAuthenticated])
class evidence(APIView):
    def get(self, request):
        round_no = latest_round()
        if round_no == 0:
            return Response(
                "No rounds completed yet.",
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            evidences = Evidence.objects.order_by("round__round_no")
            evidence_array = []
            for evidence in evidences:
                if evidence.round.round_no <= round_no:
                    evidence_array.append(
                        {
                            "round": str(evidence.round.round_no),
                            "text": str(evidence.text),
                            "image": str(evidence.image),
                        }
                    )
            return Response(
                {
                    "evidence": evidence_array,
                    "status": 200,
                }
            )


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
            print(round)
            answer = Answer.objects.filter(team=team, round=round)
            n = answer.count()
            if n == 0:
                answer = Answer(
                    team=team,
                    round=round,
                    location=request.data.get("location"),
                    victim=request.data.get("victim"),
                )
                answer.save()
                return Response(status=status.HTTP_200_OK)
            else:
                answer = answer[0]
                if answer.tries < round.tries:
                    answer.location = request.data.get("location")
                    answer.location = request.data.get("victim")
                    answer.tries += 1
                    answer.save()
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response(
                        "Number of tries are over.", status=status.HTTP_403_FORBIDDEN
                    )


@permission_classes([IsAuthenticated])
class leaderboard(APIView):
    def get(self, request, format=None):
        if check_round() == -1:
            calculate()
            round_no = latest_round()
            round = Round.objects.get(round_no=round_no)
            answers = Answer.objects.filter(round=round).order_by(
                "team__score", "submit_time"
            )
            current_rank = 1
            teams_array = []
            for answer in answers:
                answer.team.rank = current_rank
                teams_array.append(
                    {
                        "name": str(answer.team.team_name),
                        "participant1": str(answer.team.participant1),
                        "participant2": str(answer.team.participant2),
                        "participant3": str(answer.team.participant3),
                        "participant4": str(answer.team.participant4),
                        "rank": str(answer.team.rank),
                    }
                )
                current_rank += 1
            teams = Team.objects.filter(score=0).order_by("-score", "submit_time")
            for team in teams:
                team.rank = current_rank
                teams_array.append(
                    {
                        "name": str(team.team_name),
                        "participant1": str(team.participant1),
                        "participant2": str(team.participant2),
                        "participant3": str(team.participant3),
                        "participant4": str(team.participant4),
                        "rank": str(team.rank),
                    }
                )
                current_rank += 1
            return Response({"standings": teams_array, "status": 200})
        else:
            return Response(
                "Access the leaderboard after the round is over.",
                status=status.HTTP_403_FORBIDDEN,
            )


@permission_classes([IsAuthenticated])
class check(APIView):
    def get(self, request, format=None):
        return Response(
            "Registered/Logged in successfully. User is authenticated.",
            status=status.HTTP_200_OK,
        )


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
