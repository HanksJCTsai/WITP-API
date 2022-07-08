from rest_framework import viewsets
from .serializers import VPmsUserInJiraSerializer
from .models import VPmsUserInJira
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from django.db.models.functions import Upper

projectName = openapi.Parameter('projectName', in_=openapi.IN_QUERY,
                           type=openapi.TYPE_STRING, description='Project Name',)
userName = openapi.Parameter('userName', in_=openapi.IN_QUERY,
                           type=openapi.TYPE_STRING, description='User Name',)
notIncludeRole = openapi.Parameter('notIncludeRole', in_=openapi.IN_QUERY,
                           type=openapi.TYPE_ARRAY, items=openapi.TYPE_STRING, description='Not Include Role',)

# Create your views here.
class VPmsUserInJiraViewSet(viewsets.ModelViewSet):
  serializer_class = VPmsUserInJiraSerializer
  queryset = VPmsUserInJira.objects.filter()
  http_method_names = ['get', 'head']

  def get_queryset(self):
    queryset = VPmsUserInJira.objects.all().annotate(display_name_upper=Upper('display_name')).annotate(jira_name_upper=Upper('jira_name')).annotate(project_name_upper=Upper('project_name'))
    notIncludeRole = self.request.query_params.getlist('notIncludeRole', None)
    userName = self.request.query_params.get('userName')
    projectName = self.request.query_params.get('projectName')

    if projectName is not None:
      queryset = queryset.filter(project_name_upper__icontains=projectName.upper()) | queryset.filter(jira_name_upper__icontains=projectName.upper())
    if userName is not None:
      queryset = queryset.filter(display_name_upper__icontains=userName.upper())
    if len(notIncludeRole) > 0:
      queryset = queryset.exclude(project_role__in=notIncludeRole) | queryset.filter(project_role=None)

    return queryset

  @swagger_auto_schema(
    operation_summary='Get Project List',
    manual_parameters=[notIncludeRole, projectName, userName],
  )
  def list(self, request, *args, **kwargs):
    queryset = self.get_queryset()
    result = namedtuplefetchall(queryset)
    return Response(result)

def namedtuplefetchall(queryset):
    result = [
        {
            "jira_key": r.jira_key,
            "jira_project_id": r.jira_project_id,
            "jira_user_id": r.jira_user_id,
            "display_name": r.display_name,
            "pms_jira_user_id": r.pms_jira_user_id,
            "project_role": r.project_role,
            "pms_project_id": r.pms_project_id,
            "pms_user_id": r.pms_user_id,
            "division": r.division,
            "project_name": r.project_name,
            "jira_name": r.jira_name,
            "status": renderStatus(r)
        }
        for r in queryset
    ]
    return result

def renderStatus(user):
  status=0 # 帳戶正常狀態

  if user.jira_key is None and user.jira_project_id is None:
    status=1  # 帳戶已存在JIRA IT Group，但尚未存在任何PMS控管的JIRA專案內
  elif user.pms_jira_user_id is None:
    status=2 # 帳戶已存在JIRA IT Group，且已經被分配到控管的JIRA專案內，但在PMS內沒有維護
  elif user.pms_user_id is None:
    status=3 # 帳戶已存在JIRA IT Group，但是沒有存在PMS內

  return status