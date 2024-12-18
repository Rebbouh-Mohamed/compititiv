from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK
from .models import DefaultCode
from problems.models import Problem
from .serializers import DefaultCodeSerializer

class GetDefaultCode(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, problem_id, language):
        # Fetch the problem or raise 404 if not found
        problem = get_object_or_404(Problem, id=problem_id)

        # Fetch the DefaultCode object for the specific problem and language
        try:
            default_code = DefaultCode.objects.get(problem=problem, language=language)
        except DefaultCode.DoesNotExist:
            return Response(
                {"error": f"Default code for language '{language}' not found."},
                status=HTTP_404_NOT_FOUND
            )

        # Serialize the data
        serializer = DefaultCodeSerializer(default_code)

        # Return the serialized data with HTTP 200 status
        return Response(data=serializer.data, status=HTTP_200_OK)
    