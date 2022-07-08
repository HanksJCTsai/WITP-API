from rest_framework import serializers
from .models import VPmsUserInJira


class VPmsUserInJiraSerializer(serializers.ModelSerializer):
    class Meta:
        model = VPmsUserInJira
        fields = "__all__"