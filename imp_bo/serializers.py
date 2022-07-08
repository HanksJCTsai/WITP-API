from copy import error
from django.core.exceptions import ValidationError
from django.http.response import Http404
from rest_framework import serializers
from .models import ImpBo


class ImpBoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImpBo
        fields = "__all__"

    def create(self, validated_data):
        instance = ImpBo.objects.filter(bo=validated_data["bo"]).exists()
        if instance:
            raise serializers.ValidationError({"detail": "Data already exists"})
        return super().create(validated_data)
