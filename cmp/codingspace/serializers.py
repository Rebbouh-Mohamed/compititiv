from rest_framework import serializers
from .models import DefaultCode

class DefaultCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefaultCode
        fields = ['language', 'code_snippet']
