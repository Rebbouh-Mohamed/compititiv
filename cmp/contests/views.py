from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny,BasePermission
from rest_framework import status
from django.utils.timezone import now
from .models import Contest, ContestParticipation
from .serializers import ContestParticipationSerializer,ContestSerializer
from django.contrib.auth.models import User


class JoinContestView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can join contests

    def post(self, request, contest_id):
        user = request.user

        try:
            # Fetch the contest by ID
            contest = Contest.objects.get(id=contest_id)
        except Contest.DoesNotExist:
            return Response({"error": "Contest not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the contest is open for participation
        if contest.start_time > now():
            return Response({"error": "Contest has not started yet."}, status=status.HTTP_400_BAD_REQUEST)

        if contest.end_time < now():
            return Response({"error": "Contest has already ended."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user has already joined the contest
        if ContestParticipation.objects.filter(user=user, contest=contest).exists():
            return Response({"error": "You have already joined this contest."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new participation record
        participation = ContestParticipation.objects.create(user=user, contest=contest)

        serializer = ContestParticipationSerializer(participation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ContestParticipantsView(APIView):
    def get(self, request, contest_id):
        try:
            contest = Contest.objects.get(id=contest_id)
        except Contest.DoesNotExist:
            return Response({"error": "Contest not found."}, status=status.HTTP_404_NOT_FOUND)

        participations = ContestParticipation.objects.filter(contest=contest)
        serializer = ContestParticipationSerializer(participations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpContestOrComingUpContestView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        current_time = now()

        # Check for an active contest (ongoing)
        active_contest = Contest.objects.filter(start_time__lte=current_time, end_time__gte=current_time).first()

        if active_contest:
            serializer = ContestSerializer(active_contest)
            return Response({
                "status": "active",
                "contest": serializer.data
            }, status=status.HTTP_200_OK)

        # If no active contest, fetch the next upcoming contest
        upcoming_contest = Contest.objects.filter(start_time__gt=current_time).order_by('start_time').first()

        if upcoming_contest:
            serializer = ContestSerializer(upcoming_contest)
            return Response({
                "status": "upcoming",
                "contest": serializer.data
            }, status=status.HTTP_200_OK)

        # If no active or upcoming contest, return an appropriate message
        return Response({
            "status": "none",
            "message": "No active or upcoming contests at the moment."
        }, status=status.HTTP_200_OK)

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
    
    
class UserCreationView(APIView):
    permission_classes = [IsAuthenticated,IsAdminUser]

    def post(self, request):
        name = request.data.get('name')  # Extract JSON body
        password = request.data.get('password')
        
        if not name or not password:  # Check if both fields are provided
            return Response({"error": "Both name and password are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the username already exists
        if User.objects.filter(username=name).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_409_CONFLICT)
        
        # Create the user
        user = User.objects.create_user(username=name, password=password)  # Correct method for creating users
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
    