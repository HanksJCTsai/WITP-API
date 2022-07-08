from rest_framework import serializers
from .models import ImpBudln


class ImpBudlnSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImpBudln
        fields = "__all__"