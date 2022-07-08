from rest_framework import serializers
from .models import ImpPrf


class PrfSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImpPrf
        fields = "__all__"