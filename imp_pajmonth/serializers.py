from rest_framework import serializers
from .models import PajMonth


class PajMonthSerializer(serializers.ModelSerializer):
    class Meta:
        model = PajMonth
        fields = "__all__"