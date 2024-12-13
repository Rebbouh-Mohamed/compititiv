from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Submission
from problems.models import Problem,SubmitCase
from contests.models import ContestParticipation
from django.contrib.auth.models import User
from .serializers import SubmissionSerializer
from django.utils.timezone import now
import requests


class SubmitCodeView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can submit

    def post(self, request, problem_id):
        # Fetch the problem object
        problem = get_object_or_404(Problem, id=problem_id)

        # Get the contest related to the problem
        contest = problem.contest

        # Check if the contest has ended
        if contest.end_time < now():
            print(now())
            return Response({"error": "The contest has ended."}, status=status.HTTP_400_BAD_REQUEST)


        # Get the code and language submitted by the user
        user = request.user
        code = request.data.get("code")
        language = request.data.get("language")
        
        if not code:
            return Response({"error": "Code is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Test request API endpoint
        api = "http://127.0.0.1:8080/"

        
        # Fetch test cases for the problem
        submit_test_cases = SubmitCase.objects.filter(problem=problem)
        passed = 0
        for test in submit_test_cases:
            data = {
                "code": code,
                "language": language,
                "input": test.input_data,  # Input: string and number
            }

            try:
                # Make a POST request to the Codex API
                response = requests.post(api, json=data)
                response.raise_for_status()  # Raise exception for HTTP errors
                response_data = response.json()

                output = response_data.get("output", "").strip()
                if test.expected_output == output:
                    passed += 1
            except requests.exceptions.RequestException as e:
                return Response({"error": f"Error while testing the code: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Calculate percentage and points
        print("update user pts")

        percentage = passed / len(submit_test_cases) if submit_test_cases else 0
        points = problem.points * percentage

        # Save the submission in the database
        submission = Submission.objects.create(
            user=user,
            problem=problem,
            code=code,
            language=language,
            percentage=percentage * 100  # Storing percentage as a percentage (0-100)
        )

        # Update points in the ContestParticipation model
        participation, created = ContestParticipation.objects.get_or_create(user=user, contest=contest)
        participation.pionts += points
        participation.save()
    
        # Return the response with submission details
        return Response({
            'submission': {
                'id': submission.id,
                'user': submission.user.username,
                'problem': submission.problem.title,
                'code': submission.code,
                'submitted_at': submission.submitted_at,
                'percentage': submission.percentage
            }
        }, status=status.HTTP_201_CREATED)

    def get(self, request, username):
        try:
            # Fetch the user by username
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Fetch all submissions made by the user
        submissions = Submission.objects.filter(user=user)

        # Serialize and return the submissions
        serializer = SubmissionSerializer(submissions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


