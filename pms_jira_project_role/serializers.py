from rest_framework import serializers
from .models import PmsJiraProjectRole

class PmsJiraProjectRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsJiraProjectRole
        fields = "__all__"