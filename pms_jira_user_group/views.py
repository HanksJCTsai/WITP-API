from django.db import connection, transaction
from pms_jira_user_group.models import PmsJiraUserGroup
from rest_framework import viewsets
from .serializers import PmsJiraUserGroupSerializer
from .models import PmsJiraUser
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from django.http import HttpResponseBadRequest

userId = openapi.Parameter('userId', in_=openapi.IN_QUERY,
                        type=openapi.TYPE_NUMBER,
                        description='User ID',
                        required=True,
                        )

# Create your views here.
class PmsJiraUserGroupViewSet(viewsets.ModelViewSet):
    serializer_class = PmsJiraUserGroupSerializer
    queryset = PmsJiraUserGroup.objects.filter()

    def get_queryset(self):
        queryset = PmsJiraUserGroup.objects.all()
        userId = self.request.query_params.get('userId')
        queryset = queryset.filter(user_id=userId)

        return queryset

    @swagger_auto_schema(
        operation_summary='Get User Jira Group',
        manual_parameters=[userId],
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        result = namedtuplefetchall(queryset)
        return Response(result)

def namedtuplefetchall(queryset):
    if queryset is None or len(queryset) == 0:        
        result = {}
    else:
        result = {
            "id": queryset[0].id,
            "user_id": queryset[0].user_id,
            "user_name": PmsJiraUser.objects.get(id=queryset[0].user_id).user_name,
            "jira_group": [
                r.jira_group
                for r in queryset
            ]
        }
    return result