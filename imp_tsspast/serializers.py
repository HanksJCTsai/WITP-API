from rest_framework import serializers
from .models import ImpTssPast


class ImpTssPastSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImpTssPast
        fields = "__all__"