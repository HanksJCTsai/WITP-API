from rest_framework import serializers
from .models import VPmsDeleteJiraUser


class VPmsDeleteJiraUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = VPmsDeleteJiraUser
        fields = "__all__"