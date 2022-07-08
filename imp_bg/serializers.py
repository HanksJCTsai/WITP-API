from rest_framework import serializers
from .models import ImpBg


class ImpBgSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImpBg
        fields = "__all__"
