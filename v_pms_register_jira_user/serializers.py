from rest_framework import serializers
from .models import VPmsRegisterJiraUser


class VPmsRegisterJiraUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = VPmsRegisterJiraUser
        fields = "__all__"