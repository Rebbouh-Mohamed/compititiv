from django.shortcuts import render
from contests.models import ContestParticipation, Contest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from contests.serializers import ContestParticipationSerializer
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from django.shortcuts import get_object_or_404
from django.utils.timezone import now  # To compare dates

class LeaderBoard(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        # Get the active contest or the last ended contest
        contest = Contest.objects.filter(end_time__gte=now()).first()  # Active contest
        if not contest:
            contest = Contest.objects.filter(end_time__lt=now()).order_by("-end_time").first()  # Last ended contest

        if not contest:
            return Response({"error": "No active or ended contests found!"}, status=HTTP_404_NOT_FOUND)

        # Fetch leaderboard for the contest
        board = ContestParticipation.objects.filter(contest=contest).order_by("-pionts")

        if not board.exists():
            return Response({"error": "No participants found for this contest!"}, status=HTTP_204_NO_CONTENT)

        serializer = ContestParticipationSerializer(board, many=True)
        return Response({
            "contest": {
                "name": contest.title,
            },
            "leaderboard": serializer.data
        }, status=HTTP_200_OK)
