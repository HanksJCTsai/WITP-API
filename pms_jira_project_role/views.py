from django.db import connection
from rest_framework import viewsets
from .models import PmsJiraProjectRole
from .serializers import PmsJiraProjectRoleSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse

jiraProjectID = openapi.Parameter('jiraProjectID', in_=openapi.IN_QUERY,
                           type=openapi.TYPE_NUMBER, description='Jira Project ID',)

# Create your views here.
class PmsJiraProjectRoleViewSet(viewsets.ModelViewSet):
    serializer_class = PmsJiraProjectRoleSerializer
    queryset = PmsJiraProjectRole.objects.filter()    

    @swagger_auto_schema(
        operation_summary='Delete Project Role by Jira Project ID',
        manual_parameters=[jiraProjectID],
    )
    @action(detail=False, methods=["delete"])
    def delete(self, *args, **kwargs):
        jiraProjectID = self.request.query_params.get('jiraProjectID')
        # print(jiraProjectID)
        PmsJiraProjectRole.objects.filter(jira_project_id=jiraProjectID).delete()
        return HttpResponse(status=204)

    @swagger_auto_schema(
        operation_summary='Delete All Project Role',
        manual_parameters=[],
    )
    @action(detail=False, methods=["delete"])
    def delete_all(self, *args, **kwargs):
        PmsJiraProjectRole.objects.all().delete()
        return HttpResponse(status=204)