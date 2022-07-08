from rest_framework import serializers
from .models import PmsProjectVersionControl

class PmsProjectVersionControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsProjectVersionControl
        fields = "__all__"
        