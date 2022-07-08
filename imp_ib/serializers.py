from rest_framework import serializers
from .models import ImpIb


class ImpIbSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImpIb
        fields = "__all__"