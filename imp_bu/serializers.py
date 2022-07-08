from rest_framework import serializers
from .models import ImpBu


class ImpBuSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImpBu
        fields = "__all__"