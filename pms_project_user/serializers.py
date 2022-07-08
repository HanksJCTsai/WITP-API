from rest_framework import serializers
from .models import PmsProjectUser

class PmsProjectUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsProjectUser
        fields = "__all__"
        