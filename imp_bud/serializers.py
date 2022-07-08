from rest_framework import serializers
from .models import ImpBud


class ImpBudSerializer(serializers.ModelSerializer):
    # shop = serializers.CharField()
    # shop1111 = serializers.IntegerField()
    class Meta:
        model = ImpBud
        fields = "__all__"
        # fields = ("project_year", "project_name", "it_pm", "site", "plan_start", "plan_finish", "project_category", "project_type", "bu_id", "handle_div", "cancelled")
