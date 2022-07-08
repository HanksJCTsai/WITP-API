from rest_framework import serializers
from .models import PajTxt


class PajTxtSerializer(serializers.ModelSerializer):
    class Meta:
        model = PajTxt
        fields = "__all__"