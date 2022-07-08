from rest_framework import serializers
from .models import PmsSign

class PmsSignSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsSign
        fields = "__all__"