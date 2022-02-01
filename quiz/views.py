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
from django.core.exceptions import ObjectDoesNotExist
import csv


def remove(temp):
    return temp.replace(" ", "")


# def check_duration():
#     tm = timezone.now()
#     obj = Universal.objects.all().first()
#     if tm > obj.end_time:
#         Universal.objects.all().first().leaderboard_freeze = 1
#     return


def check_duration_kc():
    tm = timezone.now()
    obj = Universal.objects.all().first()
    if tm > obj.start_time and tm <= obj.end_time:
        return True
    return False


def check_round():
    tm = timezone.now()
    rounds = Round.objects.all()
    for round in rounds:
        if tm > round.start_time and tm <= round.end_time:
            return round.round_no
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
    round_no = max(latest_round(), check_round())
    team = Team.objects.get(user__username=username)
    # print(team)
    if round_no <= 5:
        team.penalty += (round_no) * 5
    else:
        team.score += (2 * round.round_no - 5) * 5
    team.save()


def calculate():
    round_no = latest_round()
    teams = Team.objects.all()
    round = Round.objects.get(round_no=round_no)
    round.check = 1
    round.save()
    if round is not None:
        for team in teams:
            answer = Answer.objects.filter(
                round_no=round_no, team=team).first()
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
                if check_ans(answer.location, round.ca_location) and check_ans(answer.victim, round.ca_victim):
                    team.submit_time = answer.submit_time
                # print(team.score)
                team.save()


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
        team = Team.objects.filter(
            team_name=request.data.get("team")["team_name"])[0]
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
                    "title": str(profile.name),
                    "data": str(profile.data),
                    "avatar_url": str(profile.image),
                }
            )
        return Response(profiles_array, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class round(APIView):
    def get(self, request):
        round_no = check_round()
        if round_no == -1:
            last_round = latest_round()
            next_round = latest_round() + 1
            flag = 0
            try:
                last_round_obj = Round.objects.get(round_no=last_round)
            except:
                last_round_obj = None
            try:
                next_round_obj = Round.objects.get(round_no=next_round)
            except:
                next_round_obj = None
            if last_round_obj is not None and next_round_obj is not None:
                team = Team.objects.get(user__username=request.user.username)
                # print("sdcs")
                # print(last_round)
                try:
                    ans = Answer.objects.get(round_no=last_round, team=team)
                except:
                    ans = None
                if ans is not None:
                    if check_ans(ans.location, last_round_obj.ca_location) and check_ans(ans.victim, last_round_obj.ca_victim):
                        flag = 1
                return Response(
                    {
                        "message": "No rounds live",
                        "correct_ans": str(last_round_obj.ca),
                        "evidence_img": str(last_round_obj.evidence_img),
                        "encrypt_img": str(last_round_obj.encrypt_img),
                        "next_round": str(next_round),
                        "next_round_start_time": str(next_round_obj.start_time),
                        "flag": str(flag),
                        "status": 200,
                    }
                )
            elif last_round_obj is not None:
                team = Team.objects.get(user__username=request.user.username)
                # print("sdcs")
                # print(last_round)
                try:
                    ans = Answer.objects.get(round_no=last_round, team=team)
                except:
                    ans = None
                if ans is not None:
                    if check_ans(ans.location, last_round_obj.ca_location) and check_ans(ans.victim, last_round_obj.ca_victim):
                        flag = 1
                return Response(
                    {
                        "message": "No rounds live",
                        "correct_ans": str(last_round_obj.ca),
                        "evidence_img": str(last_round_obj.evidence_img),
                        "encrypt_img": str(last_round_obj.encrypt_img),
                        "flag": str(flag),
                        "status": 200,
                    }
                )
            else:
                return Response(
                    {
                        "message": "No rounds live",
                        "next_round": str(next_round),
                        "next_round_start_time": str(next_round_obj.start_time),
                        "status": 200,
                    }
                )
        else:
            round = Round.objects.get(round_no=round_no)
            next_round = round_no + 1
            try:
                next_round = Round.objects.get(round_no=next_round)
                return Response(
                    {
                        "round_no": round_no,
                        "riddle": round.riddle,
                        "start_time": round.start_time,
                        "end_time": round.end_time,
                        "tries": round.tries,
                        "next_round_start_time": next_round.start_time,
                        # "location": round.ca_location,
                        # "victim": round.ca_victim,
                        "status": 200,
                    }
                )
            except ObjectDoesNotExist:
                return Response(
                    {
                        "round_no": round_no,
                        "riddle": round.riddle,
                        "start_time": round.start_time,
                        "end_time": round.end_time,
                        "tries": round.tries,
                        # "location": round.ca_location,
                        # "victim": round.ca_victim,
                        "status": 200,
                    }
                )


@permission_classes([IsAuthenticated])
class evidence(APIView):
    def get(self, request):
        round_no = latest_round()
        live_round = check_round()
        evidence_array = []
        rounds = Round.objects.order_by("round_no")
        for round in rounds:
            if round.round_no <= round_no:
                evidence_array.append(
                    {
                        "title": "ROUND " + str(round.round_no),
                        "riddle": str(round.riddle),
                        "killer_msg": str(round.killer_msg),
                        "correct_ans": str(round.ca),
                        "evidence_img": str(round.evidence_img),
                        "encrypt_img": str(round.encrypt_img)
                    }
                )
        try:
            evidence = Evidence.objects.get(round__round_no=live_round)
        except:
            evidence = None
        if evidence is not None:
            if evidence.available:
                return Response(
                    {
                        "evidences": evidence_array,
                        "killer_note": evidence.killer_note
                    }
                )
        return Response(
            {
                "evidences": evidence_array,
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
            answer = Answer.objects.filter(team=team, round_no=round.round_no)
            n = answer.count()
            if n == 0:
                answer = Answer(
                    team=team,
                    round_no=round.round_no,
                    location=request.data.get("location"),
                    victim=request.data.get("victim"),
                )
                answer.save()
                # team.submit_time = answer.submit_time
                # team.save()
                return Response({
                    "message": "Answer saved successfully.",
                    "tries_left": round.tries-1,
                    "status": 200
                })
            else:
                answer = answer[0]
                if answer.tries < round.tries:
                    answer.location = request.data.get("location")
                    answer.victim = request.data.get("victim")
                    answer.tries += 1
                    answer.save()
                    # team.submit_time = answer.submit_time
                    # team.save()
                    return Response({
                        "message": "Answer saved successfully.",
                        "tries_left": round.tries - answer.tries,
                        "status": 200
                    })
                else:
                    return Response(
                        "Number of tries are over.", status=status.HTTP_403_FORBIDDEN
                    )


@permission_classes([IsAuthenticated])
class killcode(APIView):
    def post(self, request):
        killcode = request.data.get("killcode")
        if check_duration_kc():
            if check_ans(killcode, Universal.objects.all().first().killcode):
                # lb = Universal.objects.all().first()
                # lb.leaderboard_freeze = True
                # lb.save()
                team = Team.objects.get(user__username=request.user.username)
                team.score+=1000
                team.save()
                # print(lb.leaderboard_freeze)
                return Response("correct", status=status.HTTP_200_OK)
            else:
                calculate_penalty(request.user.username)
                return Response("wrong", status=status.HTTP_200_OK)
        else:
            return Response("Time duration over.", status=status.HTTP_403_FORBIDDEN)


@permission_classes([IsAuthenticated])
class leaderboard(APIView):
    def get(self, request, format=None):
        # check_duration()
        latest = latest_round()
        try:
            latest_round_obj = Round.objects.get(round_no=latest)
        except:
            latest_round_obj = None
        if check_round() == -1:
            if latest_round_obj is not None:
                if latest_round_obj.check == 0:
                    calculate()
        teams_array = []
        current_rank = 1
        for team in Team.objects.all():
            team.final_score = team.score - team.penalty
            team.save()
        teams = Team.objects.order_by("-final_score", "submit_time")
        for team in teams:
            participant_array = [
                str(team.participant1),
                str(team.participant2),
                str(team.participant3),
                str(team.participant4),
            ]
            team.rank = current_rank
            teams_array.append(
                {
                    "name": str(team.team_name),
                    "participant_array": participant_array,
                    "score": str(team.final_score),
                    "rank": str(team.rank),
                }
            )
            team.rank = current_rank
            team.save()
            current_rank += 1
        return Response(teams_array, status=status.HTTP_200_OK)


def Leaderboard(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="leaderboard.csv"'
    writer = csv.writer(response)
    for team in Team.objects.order_by("rank"):
        writer.writerow(
            [
                team.rank,
                team.team_name,
                team.final_score,
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
