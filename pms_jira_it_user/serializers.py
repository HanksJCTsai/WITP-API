from rest_framework import serializers
from .models import PmsJiraITUser

class PmsJiraITUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsJiraITUser
        fields = "__all__"