from rest_framework import serializers
from .models import ImpPrfln


class ImpPrflnSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImpPrfln
        fields = "__all__"