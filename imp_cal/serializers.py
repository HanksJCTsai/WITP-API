from rest_framework import serializers
from .models import ImpCal


class ImpCalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImpCal
        fields = "__all__"