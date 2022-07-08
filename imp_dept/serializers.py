from rest_framework import serializers
from .models import ImpDept


class ImpDeptSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImpDept
        fields = "__all__"