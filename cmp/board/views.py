from django.shortcuts import render
from contests.models import ContestParticipation,Contest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from contests.serializers import ContestParticipationSerializer
from rest_framework.status import HTTP_200_OK,HTTP_404_NOT_FOUND,HTTP_204_NO_CONTENT
from django.shortcuts import get_object_or_404
# Create your views here.

class LeaderBoard(APIView):
    permission_classes =[IsAuthenticated]

    def get(self,request,contest_id):
        
        contest=get_object_or_404(Contest,id=contest_id)
        if not contest:
            return Response({"errore":"Contest doas not existe"},status=HTTP_404_NOT_FOUND)
        
        board=ContestParticipation.objects.filter(contest=contest).order_by("-pionts")

        if not board:
            return Response({"errore":"No Contest particaipant exists !!"},HTTP_204_NO_CONTENT)
        
        serialzer=ContestParticipationSerializer(board,many=True)
        return Response(serialzer.data,
                status=HTTP_200_OK)



