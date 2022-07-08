from rest_framework import serializers
from .models import PmsJiraUser


class PmsJiraUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsJiraUser
        fields = "__all__"