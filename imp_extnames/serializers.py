from rest_framework import serializers
from .models import extnames


class ExtnamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = extnames
        fields = "__all__"