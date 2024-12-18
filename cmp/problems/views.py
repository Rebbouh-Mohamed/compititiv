from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Contest, Problem,TestCase
from .serializers import ProblemSerializer
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from submissions.models import Submission
from rest_framework.permissions import IsAuthenticated 
from codingspace.models import DefaultCode
import requests

class ContestProblemsView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only logged-in users can access

    def get(self, request):
        # Fetch the contest
        contest = Contest.objects.filter(start_time__lte=now(), end_time__gt=now()).first()
        if not contest:
            return Response({"error": "No active contest found."}, status=status.HTTP_404_NOT_FOUND)
        # Fetch all problems for this contest
        all_problems = Problem.objects.filter(contest=contest)
# Build response data with submission status and percentage
        response_data = []
        for problem in all_problems:
            submission = Submission.objects.filter(problem=problem).first()
            try :
                code=get_object_or_404(DefaultCode,problem=problem,language='JS') 
            except:
                code=None
            submission_status = bool(submission) 
            # Calculate percentage (assuming `problem.points` defines full points)
            response_data.append({
                "id": problem.id,
                "title": problem.title,
                "level": problem.level,
                "submitted": submission_status,
                "percentage": submission.percentage if submission else 0,
                "description":problem.description,
                "input_desc":problem.input_description,
                "output_desc":problem.output_description,
                "constraint":problem.constraint,
                "input_exp":problem.input_exp,
                "output_exp":problem.output_exp,
                "codejs":code.code_snippet if code else ""
            })
        return Response(response_data, status=status.HTTP_200_OK)
    
class GetProblemView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can access

    def get(self, request, problem_id=None, problem_title=None):
        # If problem_id is provided, fetch problem by ID
        if problem_id:
            problem = get_object_or_404(Problem, id=problem_id)
        # If problem_title is provided, fetch problem by title
        elif problem_title:
            problem = get_object_or_404(Problem, title=problem_title)
        else:
            return Response({"error": "Either problem_id or problem_title must be provided."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Serialize the problem
        serializer = ProblemSerializer(problem)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TestProblem(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can submit

    def post(self, request, problem_id):
        # Fetch the problem object
        problem = get_object_or_404(Problem, id=problem_id)

        code = request.data.get("code")
        language = request.data.get("language")
        if not code:
            return Response({"error": "Code is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Test request API endpoint
        api = "http://127.0.0.1:8080/"

        # Fetch test cases for the problem
        test_cases = TestCase.objects.filter(problem=problem)
        passed = 0
        for test in test_cases:
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


        percentage = passed / len(test_cases) *100 if test_cases else 0


        # Return the response with submission details
        return Response({"percentage":percentage}, status=status.HTTP_201_CREATED)
