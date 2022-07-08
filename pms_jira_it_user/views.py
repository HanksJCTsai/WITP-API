from django.db import connection
from rest_framework import viewsets
from .models import PmsJiraITUser
from .serializers import PmsJiraITUserSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse

jiraUserID = openapi.Parameter('jiraUserID', in_=openapi.IN_QUERY,
                           type=openapi.TYPE_STRING, description='Jira User ID',)

# Create your views here.
class PmsJiraITUserViewSet(viewsets.ModelViewSet):
    serializer_class = PmsJiraITUserSerializer
    queryset = PmsJiraITUser.objects.filter()

    @swagger_auto_schema(
        operation_summary='Delete All Jira IT User',
        manual_parameters=[],
    )
    @action(detail=False, methods=["delete"])
    def delete_all(self, *args, **kwargs):
        # print(jiraProjectID)
        PmsJiraITUser.objects.all().delete()
        return HttpResponse(status=204)