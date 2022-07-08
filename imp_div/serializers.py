from rest_framework import serializers
from .models import ImpDiv


class ImpDivSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImpDiv
        fields = "__all__"