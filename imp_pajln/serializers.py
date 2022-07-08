from rest_framework import serializers
from .models import Pajln


class PajlnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pajln
        fields = "__all__"