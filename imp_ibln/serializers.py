from rest_framework import serializers
from .models import ImpIbln


class ImpIblnSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImpIbln
        fields = "__all__"