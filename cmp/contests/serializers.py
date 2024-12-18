from rest_framework import serializers
from .models import ContestParticipation,Contest
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = ['id', 'title', 'description','start_time','end_time']

class ContestParticipationSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Nested representation of the user
    class Meta:
        model = ContestParticipation
        fields = ['id', 'user','pionts']