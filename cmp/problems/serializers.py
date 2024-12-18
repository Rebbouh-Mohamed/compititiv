from rest_framework import serializers
from .models import Problem

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ['id', 'title', 'description',"input_description","output_description","constraint",
    "input_exp",
    "output_exp"]