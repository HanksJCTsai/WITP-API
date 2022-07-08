from rest_framework import serializers
from .models import ProjType


class ProjTypeySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjType
        fields = "__all__"