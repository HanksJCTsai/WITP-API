from rest_framework import serializers
from .models import PmsJiraUserGroup


class PmsJiraUserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsJiraUserGroup
        fields = "__all__"