from rest_framework import serializers
from .models import ImpTss


class ImpTssSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImpTss
        fields = "__all__"