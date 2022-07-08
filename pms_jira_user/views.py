from django.db import transaction
from pms_jira_user_group.models import PmsJiraUserGroup
from pms_project.models import PmsProject
from pms_project_user.models import PmsProjectUserLog
from pms_project_user.models import PmsProjectUser
from rest_framework import viewsets
from .serializers import PmsJiraUserSerializer
from .models import PmsJiraUser
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from datetime import datetime
from rest_framework.decorators import action
from django.http import HttpResponseBadRequest
from rest_framework.authtoken.models import Token
from django.db.models.functions import Upper

id = openapi.Parameter('id', in_=openapi.IN_QUERY,
                        type=openapi.TYPE_NUMBER, description='User ID',)
userName = openapi.Parameter('userName', in_=openapi.IN_QUERY,
                           type=openapi.TYPE_STRING, description='User Name',)
userNameList = openapi.Parameter('userNameList', in_=openapi.IN_QUERY,
                           type=openapi.TYPE_ARRAY, items=openapi.TYPE_STRING, description='User Name List',)
email = openapi.Parameter('email', in_=openapi.IN_QUERY,
                           type=openapi.TYPE_STRING, description='Email',)
emailList = openapi.Parameter('emailList', in_=openapi.IN_QUERY,
                           type=openapi.TYPE_ARRAY, items=openapi.TYPE_STRING, description='Email List',)
employeeId = openapi.Parameter('employeeId', in_=openapi.IN_QUERY,
                           type=openapi.TYPE_STRING, description='Employee ID',)
employeeIdList = openapi.Parameter('employeeIdList', in_=openapi.IN_QUERY,
                           type=openapi.TYPE_ARRAY, items=openapi.TYPE_STRING, description='Employee ID List',)
status = openapi.Parameter('status', in_=openapi.IN_QUERY,
                           type=openapi.TYPE_INTEGER, description='status',)
jiraGroup = openapi.Parameter('jiraGroup', in_=openapi.IN_QUERY,
                           type=openapi.TYPE_STRING, description='Jira Group',)


# Create your views here.
class PmsJiraUserViewSet(viewsets.ModelViewSet):
    serializer_class = PmsJiraUserSerializer
    queryset = PmsJiraUser.objects.filter()

    def get_queryset(self):
        queryset = PmsJiraUser.objects.all().annotate(user_name_upper=Upper('user_name')).annotate(employee_id_upper=Upper('employee_id'))
        userName = self.request.query_params.get('userName')
        userNameList = self.request.query_params.getlist('userNameList', None)
        email = self.request.query_params.get('email')
        emailList = self.request.query_params.getlist('emailList', None)
        employeeId = self.request.query_params.get('employeeId')
        employeeIdList = self.request.query_params.getlist('employeeIdList', None)
        status = self.request.query_params.get('status')
        jiraGroup = self.request.query_params.get('jiraGroup')
        
        if userName is not None:
            queryset = queryset.filter(user_name_upper__icontains=userName.upper())
        if len(userNameList) > 0:
            queryset = queryset.filter(user_name_upper__in=userNameList)
        if email is not None:
            queryset = queryset.filter(email_upper__icontains=email.upper())
        if len(emailList) > 0:
            queryset = queryset.filter(email__in=emailList)
        if employeeId is not None:
            queryset = queryset.filter(employee_id_upper__icontains=employeeId.upper())
        if len(employeeIdList) > 0:
            queryset = queryset.filter(employee_id_upper__in=employeeIdList)
        if status is not None:
            queryset = queryset.filter(status=status)
        if jiraGroup is not None:
            queryset = queryset.filter(pms_jira_user_group_user_id_fkey__jira_group__icontains=jiraGroup.upper())

        return queryset

    @swagger_auto_schema(
        operation_summary='Get User List',
        manual_parameters=[userName, userNameList, employeeId, employeeIdList, email, emailList, status, jiraGroup],
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        result = namedtuplefetchall(queryset)
        return Response(result)

    @swagger_auto_schema(
        operation_summary='Update User',
        manual_parameters=[],
    )
    def update(self, request, pk=None, *args, **kwargs):
        token = request.META['HTTP_AUTHORIZATION'].split(' ',)[1]
        user = Token.objects.get(key=token).user
        try:       
            with transaction.atomic(): 
                userData = PmsJiraUser.objects.get(id=pk)
                userData.user_name = request.data['user_name']
                userData.employee_id = request.data['employee_id']
                userData.email = request.data['email']
                project_user = PmsProjectUser.objects.filter(user_id=pk)
                user_group = PmsJiraUserGroup.objects.filter(user_id=pk)

                # 重新加入
                if userData.status == 2 and request.data['status'] == '1':
                    userData.add_to_org_date = datetime.now()
                    userData.deleted_date = None
                    userData.status = request.data['status']
                # 刪除
                elif userData.status == 1 and request.data['status'] == '2':
                    # print('delete')
                    userData.deleted_date = datetime.now()
                    userData.status = request.data['status']
                    # userData.jira_user_id = None
                    if len(project_user) > 0:
                        for u in project_user:
                            projectUserLog = PmsProjectUserLog.objects.create(
                                    project_user_id = u.id,
                                    project_id = u.project_id,
                                    user_id = u.user_id,
                                    project_role = u.project_role,
                                    jira_role = u.jira_role,
                                    join_date = u.join_date,
                                    action = 'DELETED',
                                    trn_user = user,
                                    approved = True,
                                    user_name = userData.user_name,
                                    employee_id = userData.employee_id,
                                    email = userData.email,
                                )

                        project_user.delete()

                    if len(user_group) > 0:
                        user_group.delete()

                userData.org_role = request.data['org_role']
                userData.save()

                serializer = PmsJiraUserSerializer(userData)
                return Response(serializer.data)

        except Exception as e:
            return HttpResponseBadRequest(e)        

    @swagger_auto_schema(
        operation_summary = 'Update User Jira ID',
        manual_parameters = [id]
    )
    @action(detail=False, methods=["post"])
    def update_jira_id(self, request):
        # 取得參數
        user_id = self.request.query_params.get('id') if self.request.query_params.get('id') is not None else request.data.get('user_id')
        jira_id = request.data.get('jira_user_id')

        # 更新 Jira ID
        user_data = PmsJiraUser.objects.get(id = user_id)
        user_data.jira_user_id = jira_id
        user_data.save()

        return Response(PmsJiraUserSerializer(user_data).data)

    @swagger_auto_schema(
        operation_summary = 'Update User Jira Group',
        manual_parameters=[id],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'jira_user_group': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.TYPE_STRING,
                    description='Jira Group'
                )
            }
        )
    )
    @action(detail=False, methods=["post"])
    def update_jira_group(self, request, pk=None, *args, **kwargs):
        # token = request.META['HTTP_AUTHORIZATION'].split(' ',)[1]
        # user = Token.objects.get(key=token).user
        
        try:       
            with transaction.atomic():
                userId = self.request.query_params.get('id')
                editGroup = request.data.get('jira_user_group')
                if userId is None or editGroup is None:
                    return HttpResponseBadRequest({})
                else:
                    userId = self.request.query_params.get('id')
                    user_data = PmsJiraUser.objects.filter(id = userId)
                    
                    PmsJiraUserGroup.objects.filter(user_id = userId).delete()
                    for value in editGroup:
                        user_data[0].pms_jira_user_group_user_id_fkey.create(
                            jira_group = value
                        )   
                        
                    return Response(namedtuplefetchall(user_data))
                    # return Response({})
        except Exception as e:
            return HttpResponseBadRequest(e)

    @action(detail=False, methods=["get"])
    def find_without_jira_id(self, request):
        user_data = PmsJiraUser.objects.filter(jira_user_id = None)
        return Response(PmsJiraUserSerializer(user_data, many=True).data)

    @action(detail=False, methods=["post"])
    def upsert(self, request, *args, **kwargs):
        # 透過Email，檢查人員是否存在
        records = filter(lambda record: record.get('email') is not None, request.data)
        records = [
            {
                "id": PmsJiraUser.objects.filter(email = record.get("email").upper())
                .first()
                .id
                if PmsJiraUser.objects.filter(email = record.get("email").upper())
                .first()
                is not None
                else None,
                **record,
                "email": record.get("email").upper(),
            }
            for record in records
        ]

        # 根據 ID 分類資料屬於 "更新" 或 "創建"
        records_to_update = []
        records_to_create = []
        [
            records_to_update.append(record)
            if record["id"] is not None
            else records_to_create.append(record)
            for record in records
        ]

        created_user = []
        try:
            with transaction.atomic():
                # 新增人員資料
                created_user = PmsJiraUser.objects.bulk_create(
                    [PmsJiraUser(**values) for values in records_to_create], batch_size = 1000
                )

                # 更新人員資料
                PmsJiraUser.objects.bulk_update(
                    [
                        PmsJiraUser(
                            id = values.get("id"),
                            user_name = values.get("user_name"),
                            employee_id = values.get("employee_id"),
                            division = values.get("division"),
                        )
                        for values in records_to_update
                    ],
                    ["user_name", "employee_id", "division"],
                    batch_size = 1000
                )
        except Exception as e:
            print(e)

        # 回傳結果
        response = {
            "update": records_to_update,
            "create": [
                PmsJiraUserSerializer(user).data
                for user in created_user
            ]
        }
        return Response(response)

def namedtuplefetchall(queryset):
    result = [
        {
            "id": r.id,
            "user_name": r.user_name,
            "employee_id": r.employee_id,
            "email": r.email,
            "status": r.status,
            "create_date": r.create_date.strftime("%Y/%m/%d %H:%M:%S"),
            "deleted_date": r.deleted_date.strftime("%Y/%m/%d %H:%M:%S") if r.deleted_date else None,
            "org_role": r.org_role,
            "jira_user_id": r.jira_user_id,
            "jira_user_group": [
                {
                    "id": t.id,
                    "user_id": t.user_id,
                    "jira_group": t.jira_group
                }
                for t in r.pms_jira_user_group_user_id_fkey.all().order_by('jira_group')
            ],
            "add_to_org_date": r.add_to_org_date.strftime("%Y/%m/%d") if r.add_to_org_date else None,
            "last_seen_in_jira": r.last_seen_in_jira.strftime("%Y/%m/%d %H:%M:%S") if r.last_seen_in_jira else None,
            "division": r.division,
            "project_list": [
                {
                    "id": s.id,
                    "project_id": s.project_id,
                    "project_name": s.project.project_name,
                    "project_role": s.project_role,
                    "jira_role": s.jira_role,
                    "join_date": s.join_date,
                }
                for s in r.pms_prj_user_user_id_fkey.filter(project__close=False).order_by('join_date')
            ],
        }
        for r in queryset
    ]
    return result