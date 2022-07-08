from rest_framework import serializers
from .models import ProjCategory


class ProjCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjCategory
        fields = "__all__"