from rest_framework import serializers
from .models import Submission
from problems.models import Problem
from django.contrib.auth.models import User
from contests.models import Contest

class SubmissionSerializer(serializers.ModelSerializer):
    # You can customize these fields if necessary
    user = serializers.StringRelatedField()  # Serializes user as a string (e.g., "username")
    problem = serializers.StringRelatedField()  # Serializes problem as a string (e.g., "problem title")
    contest = serializers.StringRelatedField()  # Serializes contest as a string (e.g., "contest title")
    
    class Meta:
        model = Submission
        fields = ['user', 'problem', 'code', 'submitted_at','language','percentage']

    