from rest_framework import serializers
from pms_project.models import PmsProjectLog


class PmsProjectLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsProjectLog
        fields = "__all__"