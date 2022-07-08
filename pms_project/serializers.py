from rest_framework import serializers
from .models import PmsProject


class PmsProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsProject
        fields = "__all__"