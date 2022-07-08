# -*- coding: utf-8 -*-

from urllib.parse import urlparse
from django.db import transaction
from django.http import HttpResponseBadRequest
from pms_jira_user.models import PmsJiraUser
from pms_project_user.models import PmsProjectUser, PmsProjectUserLog
from pms_project_version_control.models import PmsProjectVersionControl
from pms_common.views import PmsCommonViewSet
from rest_framework import viewsets
from .models import PmsProject, PmsProjectLog
from .serializers import PmsProjectSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.decorators import action
from datetime import date
from dateutil import parser
from rest_framework.authtoken.models import Token
from django.conf import settings
from rest_framework.decorators import action
from pms_common.settings import pms_settings
import requests
from django.db.models.functions import Upper
import json
import copy
from django.contrib.auth.models import User

id = openapi.Parameter('id', in_=openapi.IN_QUERY,
                           type=openapi.TYPE_NUMBER, description='Project ID',)
projectName = openapi.Parameter('projectName', in_=openapi.IN_QUERY,
                           type=openapi.TYPE_STRING, description='Project Name',)
divisions = openapi.Parameter('divisions', in_=openapi.IN_QUERY,
                           type=openapi.TYPE_ARRAY, items=openapi.TYPE_STRING, description='Divisions',)
closeProject = openapi.Parameter('closeProject', in_=openapi.IN_QUERY,
                           type=openapi.TYPE_BOOLEAN, description='Close Project',)
jiraKeys = openapi.Parameter('jiraKeys', in_=openapi.IN_QUERY,
                           type=openapi.TYPE_ARRAY, items=openapi.TYPE_STRING, description='Jira Key List',)
jiraKey = openapi.Parameter('jiraKey', in_=openapi.IN_QUERY,
                           type=openapi.TYPE_STRING, description='Jira Key',)

# Create your views here.
class PmsProjectViewSet(viewsets.ModelViewSet):
    serializer_class = PmsProjectSerializer
    queryset = PmsProject.objects.filter()
    
    def get_queryset(self):
        queryset = PmsProject.objects.all().annotate(jira_key_upper=Upper('jira_key'))
        projectName = self.request.query_params.get('projectName')
        divisions = self.request.query_params.getlist('division', None)
        closeProject = self.request.query_params.get('closeProject')
        jiraKeys = self.request.query_params.getlist('jiraKeys', None)
        
        if projectName is not None:
            queryset = queryset.filter(project_name__icontains=projectName.upper())
        if len(divisions) > 0:
            queryset = queryset.filter(division__in=divisions)
        if closeProject is not None:
            queryset = queryset.filter(close=closeProject)
        if len(jiraKeys) > 0:
            queryset = queryset.filter(jira_key_upper__in=jiraKeys)

        return queryset

    @swagger_auto_schema(
        operation_summary='Get Project List',
        manual_parameters=[projectName, divisions, closeProject, jiraKeys],
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        result = namedtuplefetchall(queryset)
        return Response(result)

    @action(detail=False, methods=["get"])
    def get_all_jira_list(self, request, pk=None):
        queryset = PmsProject.objects.all().filter(close=False)
        result = renderJiraProjectList(queryset)
        return Response(result)

    @swagger_auto_schema(
        operation_summary='Create Project',
        manual_parameters=[],
    )
    def create(self, request, pk=None, *args, **kwargs):
        token = request.META['HTTP_AUTHORIZATION'].split(' ',)[1]
        user = Token.objects.get(key=token).user
        
        try:       
            with transaction.atomic(): 
                project = PmsProject.objects.create(
                    project_name = request.data['project_name'],
                    division = request.data['division'],
                    division_supervisor = request.data['division_supervisor'],
                    division_supervisor_email = request.data['division_supervisor_email'],
                    mode = request.data['mode'],
                    product_type = request.data['product_type'],
                    plan_start = parser.parse(request.data['plan_start']).strftime("%Y-%m-%d"),
                    plan_end = parser.parse(request.data['plan_end']).strftime("%Y-%m-%d"),
                    jira_key = request.data['jira_key'],
                    jira_name = request.data['jira_name'],
                    # confluence = request.data['confluence'],
                    # confluence_key = request.data['confluence_key'],
                    # confluence_name = request.data['confluence_name'],                    
                    confluence = False,
                    confluence_key = '',
                    confluence_name = '',
                    user_contact_id = request.data['user_contact'][0]['user_id'],
                    it_contact_id = request.data['it_contact'][0]['user_id'],
                    involve_pms = request.data['involve_pms'],
                    involve_pms_start = parser.parse(request.data['involve_pms_start']).strftime("%Y-%m-%d") if request.data['involve_pms_start'] else None,
                    involve_pms_end = parser.parse(request.data['involve_pms_end']).strftime("%Y-%m-%d") if request.data['involve_pms_end'] else None,
                    project_code = request.data['project_code'],
                    create_user = user,
                    status = 0,
                    mvp_date = parser.parse(request.data['mvp_date']).strftime("%Y-%m-%d") if request.data['mvp_date'] else None,
                )
                # project.save()

                vc_body = []
                vc_html = ''
                if request.data['version_control'] is not None:
                    for value in request.data['version_control']:
                        if value['action'] == 'ADD':
                            project.pms_prj_version_control_project_id_fkey.create(
                                version_control = value['version_control'],
                                type = value['type'],
                                repo_id = value['repo_id'],
                                ut_job_name = value['ut_job_name'],
                                repo_url = value['repo_url'],
                            )
                            repoResult = checkRepo(value['version_control'], value['repo_id'], value['repo_url'], value['ut_job_name'])
                   
                            vc_body.append(
                                PmsCommonViewSet.renderVCBody(value['version_control'], value['type'], value['repo_id'],
                                    value['repo_url'], value['ut_job_name'], repoResult['repoMsg'], repoResult['repoCoverage'], value['action'])
                            )
                    if len(vc_body) > 0:
                        vc_html = PmsCommonViewSet.renderVCMailContent(vc_body)

                user_body = []
                user_html = ''
                if request.data['users'] is not None:
                    for value in request.data['users']:
                        if value['action'] == 'ADD':
                            userData = PmsJiraUser.objects.get(id=value['user_id'])
                            projectUser = project.pms_prj_user_project_id_fkey.create(
                                user_id = value['user_id'],
                                project_role = value['project_role'],
                                jira_role = value['jira_role'],
                                deleted = False,
                            )                            
                                               
                            projectUserLog = PmsProjectUserLog.objects.create(
                                project_user_id = projectUser.id,
                                project_id = project.id,
                                user_id = projectUser.user_id,
                                project_role = projectUser.project_role,
                                jira_role = projectUser.jira_role,
                                join_date = projectUser.join_date,
                                action = 'ADD',
                                trn_user = user,
                                approved = False,
                                user_name = userData.user_name,
                                employee_id = userData.employee_id,
                                email = userData.email,
                            )
                            user_body.append(
                                PmsCommonViewSet.renderUserBody(projectUser.user.user_name, projectUser.user.employee_id, projectUser.user.email,
                                    projectUser.project_role, projectUser.jira_role, 'ADD')
                            )

                    if len(user_body) > 0:
                        user_html = PmsCommonViewSet.renderUserMailContent(user_body)

                projectLog = PmsProjectLog.objects.create(
                    project_id = project.id,
                    project_name = project.project_name,
                    division = project.division,
                    division_supervisor = project.division_supervisor,
                    division_supervisor_email = project.division_supervisor_email,
                    mode = project.mode,
                    product_type = project.product_type,
                    plan_start = project.plan_start,
                    plan_end = project.plan_end,
                    jira_key = project.jira_key,
                    jira_name = project.jira_name,
                    confluence = project.confluence,
                    confluence_key = project.confluence_key,
                    confluence_name = project.confluence_name,
                    user_contact = project.user_contact.user_name,
                    user_contact_email = project.user_contact.email,
                    it_contact = project.it_contact.user_name,
                    it_contact_email = project.it_contact.email,
                    status = project.status,
                    involve_pms = project.involve_pms,
                    involve_pms_start = project.involve_pms_start,
                    involve_pms_end = project.involve_pms_end,
                    create_date = project.create_date,
                    close = project.close,
                    close_date = project.close_date,
                    approve_date = project.approve_date,
                    action = 'ADD',
                    trn_user = user,
                    project_code = request.data['project_code'],
                    create_user = project.create_user,
                    mvp_date = project.mvp_date
                )

                project_detail = PmsCommonViewSet.renderProjectBody(project, projectLog.trn_user)

                auth_user = User.objects.get(username=project.create_user)
                # 電子郵件內容樣板
                email_template = PmsCommonViewSet.renderMailContent(
                    template = 'add_project_success_to_tl',
                    userName = auth_user.username,
                    projectDetail = project_detail,
                    vcBody = vc_html,
                    userBody = user_html
                )

                PmsCommonViewSet.sendEmail(
                    '[IMP] Apply Project Successfully - ' + project.project_name,
                    email_template,
                    [auth_user.email],
                    settings.PMS_EMAIL_CC
                )
        
        except Exception as e:
            return HttpResponseBadRequest(e)

        serializer = PmsProjectSerializer(project)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary='Update Project',
        manual_parameters=[],
    )
    def update(self, request, pk=None, *args, **kwargs):
        token = request.META['HTTP_AUTHORIZATION'].split(' ',)[1]
        user = Token.objects.get(key=token).user
        try:       
            with transaction.atomic(): 
                project = PmsProject.objects.get(id=pk)
                project.project_name = request.data['project_name']
                project.division = request.data['division']
                project.division_supervisor = request.data['division_supervisor']
                project.division_supervisor_email = request.data['division_supervisor_email']
                project.mode = request.data['mode']
                project.product_type = request.data['product_type']
                project.plan_start = parser.parse(request.data['plan_start']).strftime("%Y-%m-%d")
                project.plan_end = parser.parse(request.data['plan_end']).strftime("%Y-%m-%d")
                project.jira_key = request.data['jira_key']
                project.jira_name = request.data['jira_name']
                # project.confluence = request.data['confluence']
                # project.confluence_key = request.data['confluence_key']
                # project.confluence_name = request.data['confluence_name']
                project.confluence = False
                project.confluence_key = ''
                project.confluence_name = ''
                project.user_contact_id = request.data['user_contact'][0]['user_id']
                project.it_contact_id = request.data['it_contact'][0]['user_id']
                project.involve_pms = request.data['involve_pms']
                project.involve_pms_start = parser.parse(request.data['involve_pms_start']).strftime("%Y-%m-%d") if request.data['involve_pms_start'] else None
                project.involve_pms_end = parser.parse(request.data['involve_pms_end']).strftime("%Y-%m-%d") if request.data['involve_pms_end'] else None
                project.close = request.data['close']
                if request.data['close'] is True:
                    project.close_date = date.today()
                else:
                     project.close_date = None
                project.project_code = request.data['project_code']
                project.status = 0
                project.mvp_date = parser.parse(request.data['mvp_date']).strftime("%Y-%m-%d") if request.data['mvp_date'] else None

                project.save()
                
                vc_body = []
                vc_html = ''
                if request.data['version_control'] is not None:
                    for value in request.data['version_control']:
                        if value['action'] == 'ADD':
                            projectVC = project.pms_prj_version_control_project_id_fkey.create(
                                version_control = value['version_control'],
                                type = value['type'],
                                repo_id = value['repo_id'],
                                ut_job_name = value['ut_job_name'],
                                repo_url = value['repo_url'],
                            )                 
                            repoResult = checkRepo(value['version_control'], value['repo_id'], value['repo_url'], value['ut_job_name'])
                   
                            vc_body.append(
                                PmsCommonViewSet.renderVCBody(value['version_control'], value['type'], value['repo_id'],
                                    value['repo_url'], value['ut_job_name'], repoResult['repoMsg'], repoResult['repoCoverage'], value['action'])
                            )
                        elif value['action'] == 'UPDATE':
                            projectVC = project.pms_prj_version_control_project_id_fkey.filter(id=int(value['id'])).update(
                                version_control = value['version_control'],
                                type = value['type'],
                                repo_id = value['repo_id'],
                                ut_job_name = value['ut_job_name'],
                                repo_url = value['repo_url'],
                            )                 
                            repoResult = checkRepo(value['version_control'], value['repo_id'], value['repo_url'], value['ut_job_name'])
                   
                            vc_body.append(
                                PmsCommonViewSet.renderVCBody(value['version_control'], value['type'], value['repo_id'],
                                    value['repo_url'], value['ut_job_name'], repoResult['repoMsg'], repoResult['repoCoverage'], value['action'])
                            )
                        elif value['action'] == 'DELETED':
                            projectVC = project.pms_prj_version_control_project_id_fkey.filter(id=int(value['id'])).first()
                            vc_body.append(
                                PmsCommonViewSet.renderVCBody(projectVC.version_control, projectVC.type, projectVC.repo_id,
                                    projectVC.repo_url, projectVC.ut_job_name, '', '', value['action'])
                            )
                            projectVC.delete()
                        else:
                            print('NO ACTION')

                    if len(vc_body) > 0:
                        vc_html = PmsCommonViewSet.renderVCMailContent(vc_body)

                user_body = []
                user_html = ''
                if request.data['users'] is not None:
                    for value in request.data['users']:
                        userData = PmsJiraUser.objects.get(id=value['user_id'])
                        if value['action'] == 'ADD':
                            existUser = project.pms_prj_user_project_id_fkey.filter(user_id = value['user_id']).filter(deleted=True)
                            if len(existUser) > 0:
                                existUser.delete()
                            projectUser = project.pms_prj_user_project_id_fkey.create(
                                user_id = value['user_id'],
                                project_role = value['project_role'],
                                jira_role = value['jira_role'],
                                deleted = False,
                            )                            
                            projectUserLog = PmsProjectUserLog.objects.create(
                                project_user_id = projectUser.id,
                                project_id = project.id,
                                user_id = projectUser.user_id,
                                project_role = projectUser.project_role,
                                jira_role = projectUser.jira_role,
                                join_date = projectUser.join_date,
                                action = 'ADD',
                                trn_user = user,
                                approved = False,
                                user_name = userData.user_name,
                                employee_id = userData.employee_id,
                                email = userData.email,
                            )

                            user_body.append(
                                PmsCommonViewSet.renderUserBody(projectUser.user.user_name, projectUser.user.employee_id, projectUser.user.email,
                                    projectUser.project_role, projectUser.jira_role, value['action'])
                            )
                        elif value['action'] == 'UPDATE':
                            projectUser = project.pms_prj_user_project_id_fkey.filter(id=int(value['id'])).update(
                                project_role = value['project_role'],
                                jira_role = value['jira_role'],
                                deleted = False,
                            )

                            projectUserLog = PmsProjectUserLog.objects.create(
                                project_user_id = project.pms_prj_user_project_id_fkey.get(id=int(value['id'])).id,
                                project_id = project.id,
                                user_id = project.pms_prj_user_project_id_fkey.get(id=int(value['id'])).user_id,
                                project_role = project.pms_prj_user_project_id_fkey.get(id=int(value['id'])).project_role,
                                jira_role = project.pms_prj_user_project_id_fkey.get(id=int(value['id'])).jira_role,
                                join_date = project.pms_prj_user_project_id_fkey.get(id=int(value['id'])).join_date,
                                action = 'UPDATE',
                                trn_user = user,
                                approved = False,
                                user_name = userData.user_name,
                                employee_id = userData.employee_id,
                                email = userData.email,
                            )

                            user_body.append(
                                PmsCommonViewSet.renderUserBody(project.pms_prj_user_project_id_fkey.get(id=int(value['id'])).user.user_name,
                                    project.pms_prj_user_project_id_fkey.get(id=int(value['id'])).user.employee_id,
                                    project.pms_prj_user_project_id_fkey.get(id=int(value['id'])).user.email,
                                    project.pms_prj_user_project_id_fkey.get(id=int(value['id'])).project_role,
                                    project.pms_prj_user_project_id_fkey.get(id=int(value['id'])).jira_role,
                                    value['action']
                                )
                            )
                        elif value['action'] == 'DELETED':                         
                            # projectUser = project.pms_prj_user_project_id_fkey.filter(id=int(value['id'])).first()
                            projectUser = project.pms_prj_user_project_id_fkey.filter(id=int(value['id'])).update(
                                deleted = True,
                            )
                            projectUserLog = PmsProjectUserLog.objects.create(
                                project_user_id = project.pms_prj_user_project_id_fkey.get(id=int(value['id'])).id,
                                project_id = project.id,
                                user_id = project.pms_prj_user_project_id_fkey.get(id=int(value['id'])).user_id,
                                project_role = project.pms_prj_user_project_id_fkey.get(id=int(value['id'])).project_role,
                                jira_role = project.pms_prj_user_project_id_fkey.get(id=int(value['id'])).jira_role,
                                join_date = project.pms_prj_user_project_id_fkey.get(id=int(value['id'])).join_date,
                                action = 'DELETED',
                                trn_user = user,
                                approved = False,
                                user_name = userData.user_name,
                                employee_id = userData.employee_id,
                                email = userData.email,
                            )
                            
                            user_body.append(
                                PmsCommonViewSet.renderUserBody(project.pms_prj_user_project_id_fkey.get(id=int(value['id'])).user.user_name,
                                    project.pms_prj_user_project_id_fkey.get(id=int(value['id'])).user.employee_id,
                                    project.pms_prj_user_project_id_fkey.get(id=int(value['id'])).user.email,
                                    project.pms_prj_user_project_id_fkey.get(id=int(value['id'])).project_role,
                                    project.pms_prj_user_project_id_fkey.get(id=int(value['id'])).jira_role,
                                    value['action']
                                )
                            )
                            # projectUser.delete()
                        else:
                            print('NO ACTION')

                    if len(user_body) > 0:
                        user_html = PmsCommonViewSet.renderUserMailContent(user_body)

                projectLog = PmsProjectLog.objects.create(
                    project_id = project.id,
                    project_name = project.project_name,
                    division = project.division,
                    division_supervisor = project.division_supervisor,
                    division_supervisor_email = project.division_supervisor_email,
                    mode = project.mode,
                    product_type = project.product_type,
                    plan_start = project.plan_start,
                    plan_end = project.plan_end,
                    jira_key = project.jira_key,
                    jira_name = project.jira_name,
                    confluence = project.confluence,
                    confluence_key = project.confluence_key,
                    confluence_name = project.confluence_name,
                    user_contact =  project.user_contact.user_name,
                    user_contact_email = project.user_contact.email,
                    it_contact = project.it_contact.user_name,
                    it_contact_email = project.it_contact.email,
                    status = project.status,
                    involve_pms = project.involve_pms,
                    involve_pms_start = project.involve_pms_start,
                    involve_pms_end = project.involve_pms_end,
                    create_date = project.create_date,
                    close = project.close,
                    close_date = project.close_date,
                    approve_date = project.approve_date,
                    action = 'UPDATE',
                    trn_user = user,
                    project_code = request.data['project_code'],
                    mvp_date = project.mvp_date
                )

            project = PmsProject.objects.get(id=pk)
            project_detail = PmsCommonViewSet.renderProjectBody(project, projectLog.trn_user)

            auth_user = User.objects.get(username=projectLog.trn_user)
            # 電子郵件內容樣板
            email_template = PmsCommonViewSet.renderMailContent(
                template = 'update_project_success_to_tl',
                userName = auth_user.username,
                projectDetail = project_detail,
                vcBody = vc_html,
                userBody = user_html
            )

            PmsCommonViewSet.sendEmail(
                '[IMP] Update Project Successfully - ' + project.project_name,
                email_template,
                [auth_user.email],
                settings.PMS_EMAIL_CC
            )

            serializer = PmsProjectSerializer(project)
            return Response(serializer.data)
        except Exception as e:
            return HttpResponseBadRequest(e)
    
    @swagger_auto_schema(
        operation_summary='Update Project Create Jira Status',
        manual_parameters=[id],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'create_result': openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    description='Create Result. 0: Check Failed. 1: Ready for Create User ID. 2: Ready for Create Project'
                ),
                'jira_key': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='JIRA Key'
                ),
                'remark': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Remark'
                )
            }
        )
    )
    @action(detail=False, methods=["post"])
    def update_create_result(self, request, pk=None):
        token = request.META['HTTP_AUTHORIZATION'].split(' ',)[1]
        user = Token.objects.get(key=token).user
        
        projectId = self.request.query_params.get('id')
        project = PmsProject.objects.get(id=projectId)
        createResult = request.data.get('create_result')
        jiraKey = request.data.get('jira_key')
        remark = request.data.get('remark')
        
        if createResult == 1:
            # ready for create Jira User
            project.status = 5
            project.save()
        elif createResult == 2:
            # ready for create Jira Project            
            with transaction.atomic(): 
                if project.jira_key != jiraKey:
                    project.jira_key = jiraKey
                msg = create_jira_project(project)
                if msg['success'] is True:
                    project.jira_project_id = msg['jiraId']
                    project.status = 6
                    print('Successfully! Send Mail')
                    project.save()

                    add_user_result = []
                    delete_user_result = []
                    role_ids = get_role_id(msg['jiraId'])
                    if role_ids['success'] == True:
                        # 新增Porject User
                        admin_role_id = [x for x in role_ids['roleIds'] if x['role'] == pms_settings.JIRA_PROJECT_ADMIN["AdminProjectRole"]]
                        admin_user_list = []
                        admin_user_list = copy.deepcopy(pms_settings.JIRA_PROJECT_ADMIN["AdminUserList"])
                        # 將TL加入Admin List
                        admin_user_list.append({
                            "Name": project.it_contact.user_name,
                            "JiraId": project.it_contact.jira_user_id
                        })

                        # 刪除Porject User
                        for user in project.pms_prj_user_project_id_fkey.filter(deleted=True):
                            deleted = True
                            for id in role_ids['roleIds']:
                                users_in_role = get_user_in_role(msg['jiraId'], id['roleId'])['users']
                                if len([x for x in users_in_role if x['actorUser']['accountId'] == user.user.jira_user_id])>0:
                                    deleteResult = delete_user_from_project(msg['jiraId'], id['roleId'], user.user.jira_user_id)
                                    if deleteResult['success'] == True:
                                        delete_user_result.append("Delete {user} from Jira project Successfully!".format(user = user.user.user_name))
                                    else:
                                        delete_user_result.append("Delete {user} from Jira project Failed! Reson: {reason}".format(user = user.user.user_name, reason=deleteResult['msg']))
                                        deleted = False
                            if deleted == True:
                                print(user.id)
                                user.delete()
                        # 加入Admin
                        for id in admin_role_id:
                            users_in_role = get_user_in_role(msg['jiraId'], id['roleId'])['users']
                            for value in admin_user_list:
                                if len([x for x in users_in_role if x['actorUser']['accountId'] == value['JiraId']])<=0:
                                    addResult = add_user_into_project(msg['jiraId'], id['roleId'], value['JiraId'])
                                    if addResult['success'] == True:
                                        add_user_result.append("{user} add into Jira Admin Successfully!".format(user = value['Name']))
                                    else:
                                        add_user_result.append("{user} add into Jira Admin Failed! Reson: {reason}".format(user = value['Name'], reason=addResult['msg']))
                        # 加入Default Role
                        for role in pms_settings.JIRA_PROJECT_DEFAULT_ROLE["ProjectRole"]:
                            role_id = [x for x in role_ids['roleIds'] if x['role'] == role]
                            for id in role_id:
                                users_in_role = get_user_in_role(msg['jiraId'], id['roleId'])['users']
                                for user in project.pms_prj_user_project_id_fkey.filter(deleted=False):
                                    if len([x for x in users_in_role if x['actorUser']['accountId'] == user.user.jira_user_id])<=0:
                                        addResult = add_user_into_project(msg['jiraId'], id['roleId'], user.user.jira_user_id)
                                        if addResult['success'] == True:
                                            add_user_result.append("{user} add into Jira default role Successfully!".format(user = user.user.user_name))
                                        else:
                                            add_user_result.append("{user} add into Jira default role Failed! Reson: {reason}".format(user = user.user.user_name, reason=addResult['msg']))

                    else:
                        print(role_ids['msg'])
                        return HttpResponseBadRequest(role_ids['msg']) 

                    data = [add_user_result, delete_user_result]
                    auth_user = User.objects.get(username=project.create_user)
                    # 電子郵件內容樣板
                    email_template = PmsCommonViewSet.renderMailContent(
                        template = 'create_jira_success_to_tl',
                        userName = auth_user.username,
                        jiraKey = project.jira_key,
                        remark = remark,
                        data = data,
                    )
                    # print(email_template)
                    
                    PmsCommonViewSet.sendEmail(
                        '[IMP] Jira Create Successfully - ' + project.project_name,
                        email_template,
                        [auth_user.email],
                        settings.PMS_EMAIL_CC
                    )
                else:
                    return HttpResponseBadRequest(msg['msg'])                         
            
        elif createResult == 0:
            print('Failed! Send Mail')
            project.status = 0
            project.save()
            
            auth_user = User.objects.get(username=project.create_user)
            # 電子郵件內容樣板
            email_template = PmsCommonViewSet.renderMailContent(
                template = 'create_jira_failed_to_tl',
                userName = auth_user.username,
                jiraKey = project.jira_key,
                remark = remark
            )

            PmsCommonViewSet.sendEmail(
                '[IMP] Jira Create Failed - ' + project.project_name,
                email_template,
                [auth_user.email],
                settings.PMS_EMAIL_CC
            )

        return Response({})


    @action(detail=False, methods=["post"])
    def upsert(self, request, *args, **kwargs):
        # 取得 Token 並解析出 User
        token = request.META['HTTP_AUTHORIZATION'].split(' ',)[1]
        maintainer = 'anonymous'
        try:
            maintainer = Token.objects.get(key = token).user
        except:
            print('Token matching query does not exist.')

        # 透過專案名稱及代碼，檢查專案是否存在
        records = filter(filter_invalid_upserted_project, request.data)
        records = [
            {
                "id": PmsProject.objects.filter(project_name = record.get("project_name"))
                .first()
                .id
                if PmsProject.objects.filter(project_name = record.get("project_name"))
                .first()
                is not None
                else None,
                **record,
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

        # 新增專案資料
        for project in records_to_create:
            try:
                with transaction.atomic():
                    # 建立專案
                    created_project = PmsProject.objects.create(
                        project_name = project.get('project_name'),
                        division = project.get('division'),
                        division_supervisor = project.get('division_supervisor'),
                        division_supervisor_email = project.get('division_supervisor_email'),
                        mode = project.get('mode'),
                        product_type = project.get('product_type'),
                        plan_start = parser.parse(project.get('plan_start')).strftime("%Y-%m-%d"),
                        plan_end = parser.parse(project.get('plan_end')).strftime("%Y-%m-%d"),
                        jira_key = project.get('jira_key'),
                        jira_name = project.get('jira_name'),
                        # confluence = project.get('confluence'),
                        # confluence_key = project.get('confluence_key'),
                        # confluence_name = project.get('confluence_name'),
                        confluence = False,
                        confluence_key = '',
                        confluence_name = '',
                        user_contact_id = project.get('user_contact')[0]['user_id'],
                        it_contact_id = project.get('it_contact')[0]['user_id'],
                        involve_pms = project.get('involve_pms'),
                        involve_pms_start = parser.parse(project.get('involve_pms_start')).strftime("%Y-%m-%d") if project.get('involve_pms_start') else None,
                        involve_pms_end = parser.parse(project.get('involve_pms_end')).strftime("%Y-%m-%d") if project.get('involve_pms_end') else None,
                        project_code = project.get('project_code'),
                        create_user = maintainer,
                        status = 0,
                    )

                    # 建立專案新增日誌
                    created_project_log = PmsProjectLog.objects.create(
                        project_id = created_project.id,
                        project_name = created_project.project_name,
                        division = created_project.division,
                        division_supervisor = created_project.division_supervisor,
                        division_supervisor_email = created_project.division_supervisor_email,
                        mode = created_project.mode,
                        product_type = created_project.product_type,
                        plan_start = created_project.plan_start,
                        plan_end = created_project.plan_end,
                        jira_key = created_project.jira_key,
                        jira_name = created_project.jira_name,
                        confluence = created_project.confluence,
                        confluence_key = created_project.confluence_key,
                        confluence_name = created_project.confluence_name,
                        user_contact = created_project.user_contact.user_name,
                        user_contact_email = created_project.user_contact.email,
                        it_contact = created_project.it_contact.user_name,
                        it_contact_email = created_project.it_contact.email,
                        status = created_project.status,
                        involve_pms = created_project.involve_pms,
                        involve_pms_start = created_project.involve_pms_start,
                        involve_pms_end = created_project.involve_pms_end,
                        create_date = created_project.create_date,
                        close = created_project.close,
                        close_date = created_project.close_date,
                        approve_date = created_project.approve_date,
                        action = 'ADD',
                        trn_user = maintainer,
                        project_code = created_project.project_code,
                        create_user = created_project.create_user,
                        mvp_date = created_project.mvp_date
                    )

                    # 建立專案版本控制資訊
                    vc_body = []
                    vc_html = ''
                    if project.get('version_control') is not None:
                        for version in project.get('version_control'):
                            PmsProjectVersionControl.objects.create(
                                project_id = created_project.id,
                                version_control = version.get('version_control'),
                                type = version.get('type'),
                                repo_id = version.get('repo_id'),
                                ut_job_name = version.get('ut_job_name'),
                                repo_url = version.get('repo_url'),
                            )
                            
                            repoResult = checkRepo(version.get('version_control'), version.get('repo_id'), version.get('repo_url'), version.get('ut_job_name'))
                   
                            vc_body.append(
                                PmsCommonViewSet.renderVCBody(version.get('version_control'), version.get('type'), version.get('repo_id'),
                                    version.get('repo_url'), version.get('ut_job_name'), repoResult['repoMsg'], repoResult['repoCoverage'], 'ADD')
                            )

                        if len(vc_body) > 0:
                            vc_html = PmsCommonViewSet.renderVCMailContent(vc_body)

                    # 建立專案成員資訊
                    user_body = []
                    user_html = ''
                    if project.get('users') is not None:
                        for user in project.get('users'):
                            try:
                                jira_user = PmsJiraUser.objects.get(user_name = user.get('user_name')) 
                                jira_user = jira_user if jira_user is not None else PmsJiraUser.objects.get(employee_id = user.get('employee_id'))
                                if jira_user is None:
                                    continue

                                created_user = PmsProjectUser.objects.create(
                                    user_id = jira_user.id,
                                    project_id = created_project.id,
                                    project_role = user.get('project_role'),
                                    jira_role = user.get('jira_role'),
                                    deleted = False,
                                )
                            
                                user_body.append(
                                    PmsCommonViewSet.renderUserBody(
                                        jira_user.user_name,
                                        jira_user.employee_id,
                                        jira_user.email,
                                        created_user.project_role,
                                        created_user.jira_role,
                                        'ADD'
                                    )
                                )

                                projectUserLog = PmsProjectUserLog.objects.create(
                                    project_user_id = created_user.id,
                                    project_id = created_project.id,
                                    user_id = created_user.user_id,
                                    project_role = created_user.project_role,
                                    jira_role = created_user.jira_role,
                                    action = 'UPDATE',
                                    trn_user = maintainer,
                                    approved = False,
                                    user_name = jira_user.user_name,
                                    employee_id = jira_user.employee_id,
                                    email = jira_user.email,
                                )
                            except Exception as e:
                                print(e)

                        if len(user_body) > 0:
                            user_html = PmsCommonViewSet.renderUserMailContent(user_body)

                    project_detail = PmsCommonViewSet.renderProjectBody(created_project, created_project_log.trn_user)                    

                    auth_user = User.objects.get(username=created_project.create_user)
                    # 電子郵件內容樣板
                    email_template = PmsCommonViewSet.renderMailContent(
                        template = 'add_project_success_to_tl',
                        userName = auth_user.username,
                        projectDetail = project_detail,
                        vcBody = vc_html,
                        userBody = user_html
                    )

                    PmsCommonViewSet.sendEmail(
                        '[IMP] Apply Project Successfully - ' + created_project.project_name,
                        email_template,
                        [auth_user.email],
                        settings.PMS_EMAIL_CC
                    )

            except Exception as e:
                print(e)
                return HttpResponseBadRequest(e)

        # 更新專案
        try:
            with transaction.atomic():
                # 批量更新專案
                PmsProject.objects.bulk_update(
                    [
                        PmsProject(
                            id = values.get("id"),
                            project_code = values.get("project_code"),
                            division = values.get('division'),
                            division_supervisor = values.get('division_supervisor'),
                            division_supervisor_email = values.get('division_supervisor_email'),
                            mode = values.get('mode'),
                            product_type = values.get('product_type'),
                            plan_start = parser.parse(values.get('plan_start')).strftime("%Y-%m-%d"),
                            plan_end = parser.parse(values.get('plan_end')).strftime("%Y-%m-%d"),
                            user_contact_dd = values.get('user_contact')[0]['user_id'],
                            it_contact_id = values.get('it_contact')[0]['user_id'],
                            involve_pms = values.get('involve_pms'),
                            involve_pms_start = parser.parse(values.get('involve_pms_start')).strftime("%Y-%m-%d") if values.get('involve_pms_start') else None,
                            involve_pms_end = parser.parse(values.get('involve_pms_end')).strftime("%Y-%m-%d") if values.get('involve_pms_end') else None,
                            status = 0,
                            mvp_date = parser.parse(values.get('mvp_date')).strftime("%Y-%m-%d") if values.get('mvp_date') else None
                        )
                        for values in records_to_update
                    ],
                    [
                        "project_code",
                        "division",
                        "division_supervisor",
                        "division_supervisor_email",
                        "mode",
                        "product_type",
                        "plan_start",
                        "plan_end",
                        "user_contact_id",
                        "it_contact_id",
                        "involve_pms",
                        "involve_pms_start",
                        "involve_pms_end",
                        "status",
                        "mvp_date"
                    ],
                    batch_size = 1000
                )

                for project in records_to_update:
                    # 建立專案新增日誌
                    specific_project = PmsProject.objects.filter(id = project.get('id'))[0]
                    created_project_log = PmsProjectLog.objects.create(
                        project_id = specific_project.id,
                        project_name = specific_project.project_name,
                        division = specific_project.division,
                        division_supervisor = specific_project.division_supervisor,
                        division_supervisor_email = specific_project.division_supervisor_email,
                        mode = specific_project.mode,
                        product_type = specific_project.product_type,
                        plan_start = specific_project.plan_start,
                        plan_end = specific_project.plan_end,
                        jira_key = specific_project.jira_key,
                        jira_name = specific_project.jira_name,
                        confluence = specific_project.confluence,
                        confluence_key = specific_project.confluence_key,
                        confluence_name = specific_project.confluence_name,
                        user_contact = specific_project.user_contact.user_name,
                        user_contact_email = specific_project.user_contact.email,
                        it_contact = specific_project.it_contact.user_name,
                        it_contact_email = specific_project.it_contact.email,
                        status = specific_project.status,
                        involve_pms = specific_project.involve_pms,
                        involve_pms_start = specific_project.involve_pms_start,
                        involve_pms_end = specific_project.involve_pms_end,
                        create_date = specific_project.create_date,
                        close = specific_project.close,
                        close_date = specific_project.close_date,
                        approve_date = specific_project.approve_date,
                        action = 'UPDATE',
                        trn_user = maintainer,
                        project_code = specific_project.project_code,
                        create_user = specific_project.create_user,
                        mvp_date = specific_project.mvp_date
                    )

                    # 更新專案版本控制資訊
                    vc_body = []
                    vc_html = ''
                    if project.get('version_control') is not None:
                        PmsProjectVersionControl.objects.filter(project_id = project.get('id')).delete()
                        for version in project.get('version_control'):
                            PmsProjectVersionControl.objects.create(
                                project_id = project.get('id'),
                                version_control = version.get('version_control'),
                                type = version.get('type'),
                                repo_id = version.get('repo_id'),
                                ut_job_name = version.get('ut_job_name'),
                                repo_url = version.get('repo_url'),
                            )
                            repoResult = checkRepo(version.get('version_control'), version.get('repo_id'), version.get('repo_url'), version.get('ut_job_name'))
                   
                            vc_body.append(
                                PmsCommonViewSet.renderVCBody(version.get('version_control'), version.get('type'), version.get('repo_id'),
                                    version.get('repo_url'), version.get('ut_job_name'), repoResult['repoMsg'], repoResult['repoCoverage'], 'UPDATE')
                            )

                        if len(vc_body) > 0:
                            vc_html = PmsCommonViewSet.renderVCMailContent(vc_body)
                    
                    # 更新專案成員資訊
                    user_body = []
                    user_html = ''
                    if project.get('users') is not None:
                        PmsProjectUser.objects.filter(project_id = project.get('id')).update(deleted = True)
                        for user in project.get('users'):
                            try:
                                jira_user = PmsJiraUser.objects.get(user_name = user.get('user_name')) 
                                jira_user = jira_user if jira_user is not None else PmsJiraUser.objects.get(employee_id = user.get('employee_id'))
                                if jira_user is None:
                                    continue

                                operate = 'UPDATE'
                                created_user = PmsProjectUser.objects.filter(project_id = project.get('id')).filter(user_id = jira_user.id).update(deleted = False)
                                if len(created_user) <= 0:
                                    created_user = PmsProjectUser.objects.create(
                                        user_id = jira_user.id,
                                        project_id = project.get('id'),
                                        project_role = user.get('project_role'),
                                        jira_role = user.get('jira_role'),
                                            deleted = False,
                                    )
                                    operate = 'ADD'
                            
                                user_body.append(
                                    PmsCommonViewSet.renderUserBody(
                                        jira_user.user_name,
                                        jira_user.employee_id,
                                        jira_user.email,
                                        created_user.project_role,
                                        created_user.jira_role,
                                        operate,
                                    )
                                )

                                projectUserLog = PmsProjectUserLog.objects.create(
                                    project_user_id = created_user.id,
                                    project_id = project.get('id'),
                                    user_id = created_user.user_id,
                                    project_role = created_user.project_role,
                                    jira_role = created_user.jira_role,
                                    action = operate,
                                    trn_user = maintainer,
                                    approved = False,
                                    user_name = jira_user.user_name,
                                    employee_id = jira_user.employee_id,
                                    email = jira_user.email,
                                )
                            except Exception as e:
                                print(e)

                        if len(user_body) > 0:
                            user_html = PmsCommonViewSet.renderUserMailContent(user_body)

                    project_detail = PmsCommonViewSet.renderProjectBody(specific_project, created_project_log.trn_user)

                    auth_user = User.objects.get(username=created_project_log.trn_user)
                    # 電子郵件內容樣板
                    email_template = PmsCommonViewSet.renderMailContent(
                        template = 'update_project_success_to_tl',
                        userName = auth_user.username,
                        projectDetail = project_detail,
                        vcBody = vc_html,
                        userBody = user_html
                    )

                    PmsCommonViewSet.sendEmail(
                        '[IMP] Update Project Successfully - ' + specific_project.project_name,
                        email_template,
                        [auth_user.email],
                        settings.PMS_EMAIL_CC
                    )

        except Exception as e:
            print(e)
            return HttpResponseBadRequest(e)

        # 回傳結果
        response = {
            "update": records_to_update,
            "create": records_to_create
        }
        return Response(response)


    @swagger_auto_schema(
        operation_summary='Validate Jira Key',
        manual_parameters=[jiraKey],
    )
    @action(detail=False, methods=["get"])
    def validate_jira_key(self, request, pk=None):
        jiraKey = self.request.query_params.get('jiraKey')
        result = validate_jira_key(jiraKey)
        return Response(result)

    def getProjectDetail(queryset):
        return namedtuplefetchall(queryset)

def renderJiraProjectList(queryset):
    result = [
        {
            "id": r.id,
            "project_name": r.project_name,
            "jira_key": r.jira_key,
            "jira_name": r.jira_name,
            "jira_project_id": r.jira_project_id,
        }
        for r in queryset
    ]
    return result

def namedtuplefetchall(queryset):
    result = [
        {
            "id": r.id,
            "project_name": r.project_name,
            "project_code": r.project_code,
            "division": r.division,
            "division_supervisor": r.division_supervisor,
            "division_supervisor_email": r.division_supervisor_email,
            "mode": r.mode,
            "product_type": r.product_type,
            "plan_start": r.plan_start.strftime("%Y/%m/%d") if r.plan_start else None,
            "plan_end": r.plan_end.strftime("%Y/%m/%d") if r.plan_end else None,
            "jira_key": r.jira_key,
            "jira_name": r.jira_name,
            "confluence": r.confluence,
            "confluence_key": r.confluence_key,
            "confluence_name": r.confluence_name,
            "mvp_date": r.mvp_date,
            "jira_project_id": r.jira_project_id,
            "user_contact": [
                {
                    "user_id": r.user_contact.id,
                    "user_name": r.user_contact.user_name,
                    "employee_id": r.user_contact.employee_id,
                    "email": r.user_contact.email
                }                
            ],
            "it_contact": [
                {
                    "user_id": r.it_contact.id,
                    "user_name": r.it_contact.user_name,
                    "employee_id": r.it_contact.employee_id,
                    "email": r.it_contact.email
                }                
            ],
            "status": r.status,
            "involve_pms": r.involve_pms,
            "involve_pms_start": r.involve_pms_start.strftime("%Y/%m/%d") if r.involve_pms_start else None,
            "involve_pms_end": r.involve_pms_end.strftime("%Y/%m/%d") if r.involve_pms_end else None,
            "create_date": r.create_date.strftime("%Y/%m/%d %H:%M:%S") if r.create_date else None,
            "create_user": r.create_user,
            "close": r.close,
            "close_date": r.close_date.strftime("%Y/%m/%d %H:%M:%S") if r.close_date else None,
            "approve_date": r.approve_date.strftime("%Y/%m/%d %H:%M:%S") if r.approve_date else None,
            "version_control": [
                {
                    "id": s.id,
                    "project_id": s.project_id,
                    "version_control": s.version_control,
                    "type": s.type,
                    "repo_id": s.repo_id,
                    "ut_job_name": s.ut_job_name,
                    "repo_url": s.repo_url,
                }
                for s in r.pms_prj_version_control_project_id_fkey.all()
            ],
            "users": [
                {
                    "id": t.id,
                    "project_id": t.project_id,
                    "user_id": t.user_id,
                    "user_name": t.user.user_name,
                    "employee_id": t.user.employee_id,
                    "email": t.user.email,
                    "project_role": t.project_role,
                    "jira_user_id": t.user.jira_user_id,
                    "jira_role": t.jira_role,
                    "join_date": t.join_date.strftime("%Y/%m/%d") if t.join_date else None,                    
                    "jira_user_group": [
                        {
                            "id": u.id,
                            "user_id": u.user_id,
                            "jira_group": u.jira_group
                        }
                        for u in t.user.pms_jira_user_group_user_id_fkey.all().order_by('jira_group')
                    ],
                }
                for t in r.pms_prj_user_project_id_fkey.filter(deleted=False)
            ],
            "logs": [
                {
                    "id": l.id,
                    "project_id": l.project_id,
                    "action": l.action,
                    "trn_date": l.trn_date.strftime("%Y/%m/%d %H:%M:%S") if l.trn_date else None,
                }
                for l in PmsProjectLog.objects
                    .filter(project_id=r.id)
                    .order_by('-trn_date')[:1]
            ],
        }
        for r in queryset
    ]
    return result

def filter_invalid_upserted_project(record):
    if record.get("involve_pms"): 
        if record.get("involve_pms_start") is not None and record.get("involve_pms_end") is not None: 
            return True
        else: 
            return False
    else:
        return True

def validate_jira_key(jiraKey):
    returnMsg = {
        'success': False,
        'msg': '',
    }
    headers = {
            'Authorization': 'Basic {token}'.format(token=pms_settings.JIRA_HOST_TOKEN["Token"]),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    proxies = pms_settings.PROXIES
    try: 
        path = '{jira_host}{api_path}'.format(jira_host=pms_settings.JIRA_HOST_TOKEN["Host"],
            api_path=pms_settings.JIRA_HOST_TOKEN["ValidateJiraKey"].format(jiraKey = jiraKey))
        requests.packages.urllib3.disable_warnings()
        r = requests.get(
            path,
            verify=False,
            proxies=proxies,
            headers=headers)
        print(r.json())
        if r.status_code == 200:
            if len(r.json()['errors']):
                returnMsg['success'] = False
                returnMsg['msg'] = r.json()['errors']['projectKey']
            else:
                returnMsg['success'] = True
        else:
            returnMsg['success'] = False
            returnMsg['msg'] = 'Call Jira API failed, Status code: {statusCode}, message: {message}'.format(statusCode=r.status_code, message=r.json())
                    
    except Exception as e:
        print(e)
        returnMsg['success'] = False
        returnMsg['msg'] = 'Call Jira API Error: {}'.format(e)
    return returnMsg

def create_jira_project(project):
    returnMsg = {
        'success': False,
        'msg': '',
        'jiraId': 0
    }
    if project.jira_project_id is None:        
        headers = {
            'Authorization': 'Basic {token}'.format(token=pms_settings.JIRA_HOST_TOKEN["Token"]),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        proxies = pms_settings.PROXIES

        try: 
            path = '{jira_host}{api_path}'.format(jira_host=pms_settings.JIRA_HOST_TOKEN["Host"],
                api_path=pms_settings.JIRA_HOST_TOKEN["CreateProject"])
            # print(path)
            
            if project.it_contact.jira_user_id is None or project.it_contact.jira_user_id == "":
                raise Exception("The Tech Leader has no jira account, pleas check.")

            payload = {
                "description": project.project_name,
                "leadAccountId": project.it_contact.jira_user_id,
                "projectTemplateKey": "com.pyxis.greenhopper.jira:gh-simplified-agility-scrum",
                "name": project.jira_name,
                "projectTypeKey": "software",
                "assigneeType": "UNASSIGNED",
                "key": project.jira_key
            }

            requests.packages.urllib3.disable_warnings()
            r = requests.post(
                path,
                verify=False,
                proxies=proxies,
                headers=headers,
                data=json.dumps(payload)
            )
                
            if r.status_code == 201:
                returnMsg['success'] = True
                returnMsg['msg'] = ''
                returnMsg['jiraId'] = r.json()['id']
            else:
                # returnMsg ='Call Jira API failed, Status code: {statusCode}, message: {message}'.format(statusCode=r.status_code, message=r.json())
                returnMsg['success'] = False
                returnMsg['msg'] = 'Call Jira API failed, Status code: {statusCode}, message: {message}'.format(statusCode=r.status_code, message=r.json())
                    
        except Exception as e:
            print(e)
            returnMsg['success'] = False
            returnMsg['msg'] = 'Call Jira API Error: {}'.format(e)
    else:
        returnMsg['success'] = True
        returnMsg['msg'] = 'No need to create Jira'
        returnMsg['jiraId'] = project.jira_project_id

    return returnMsg

def get_role_id(jira_project):
    returnMsg = {
        'success': False,
        'msg': '',
        'roleIds': []
    }
    headers = {
        'Authorization': 'Basic {token}'.format(token=pms_settings.JIRA_HOST_TOKEN["Token"]),
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    proxies = pms_settings.PROXIES
    try: 
        path = '{jira_host}{api_path}'.format(jira_host=pms_settings.JIRA_HOST_TOKEN["Host"],
            api_path=pms_settings.JIRA_HOST_TOKEN["GetProjectRole"].format(projectIdOrKey = jira_project))
        requests.packages.urllib3.disable_warnings()
        r = requests.get(
            path,
            verify=False,
            proxies=proxies,
            headers=headers)

        if r.status_code == 200:
            returnMsg['success'] = True
            for key, value in r.json().items():
                # print(value)
                if key not in pms_settings.JIRA_PROJECT_SKIP_ROLE["ProjectRole"]:
                    path = value.split('/')
                    returnMsg['roleIds'].append({"role": key, "roleId": path[len(path)-1]})
        else:
            returnMsg['success'] = False
            returnMsg['msg'] = 'Get Role ID failed, Status code: {statusCode}, message: {message}'.format(statusCode=r.status_code, message=r.json())
                    
    except Exception as e:
        print(e)
        returnMsg['success'] = False
        returnMsg['msg'] = 'Call Jira API Error: {}'.format(e)

    return returnMsg

def get_user_in_role(jira_project, role_id):
    returnMsg = {
        'success': False,
        'msg': '',
        'users': []
    }
    headers = {
        'Authorization': 'Basic {token}'.format(token=pms_settings.JIRA_HOST_TOKEN["Token"]),
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    proxies = pms_settings.PROXIES
    path = '{jira_host}{api_path}'.format(jira_host=pms_settings.JIRA_HOST_TOKEN["Host"],
        api_path=pms_settings.JIRA_HOST_TOKEN["GetProjectRoleByID"].format(projectIdOrKey = jira_project, projectRoleId = role_id))
    # print(path)

    try:
        requests.packages.urllib3.disable_warnings()
        r = requests.get(
            path,
            verify=False,
            proxies=proxies,
            headers=headers,
        )

        if r.status_code == 200:
            returnMsg['success'] = True
            returnMsg['msg'] = ''
            returnMsg['users'] = r.json()['actors']
        else:
            returnMsg['success'] = False
            returnMsg['msg'] = 'Add User Into Role Failed, Status code: {statusCode}, message: {message}'.format(statusCode=r.status_code, message=r.json())
    except Exception as e:
        print(e)
        returnMsg['success'] = False
        returnMsg['msg'] = 'Call Jira API Error: {}'.format(e)  
    return returnMsg            

def add_user_into_project(jira_project, role_id, jira_user_id):
    returnMsg = {
        'success': False,
        'msg': ''
    }
    headers = {
        'Authorization': 'Basic {token}'.format(token=pms_settings.JIRA_HOST_TOKEN["Token"]),
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    proxies = pms_settings.PROXIES
    path = '{jira_host}{api_path}'.format(jira_host=pms_settings.JIRA_HOST_TOKEN["Host"],
        api_path=pms_settings.JIRA_HOST_TOKEN["AssignUserIntoProjectRole"].format(projectIdOrKey = jira_project, projectRoleId = role_id))
    # print(path)
    
    payload = {
        "user": [jira_user_id]
    }

    try:
        requests.packages.urllib3.disable_warnings()
        r = requests.post(
            path,
            verify=False,
            proxies=proxies,
            headers=headers,
            data=json.dumps(payload)
        )

        if r.status_code == 200:
            returnMsg['success'] = True
            returnMsg['msg'] = ''
        else:
            returnMsg['success'] = False
            returnMsg['msg'] = 'Add User Into Role Failed, Status code: {statusCode}, message: {message}'.format(statusCode=r.status_code, message=r.json())
    except Exception as e:
        print(e)
        returnMsg['success'] = False
        returnMsg['msg'] = 'Call Jira API Error: {}'.format(e)  
    return returnMsg            

def delete_user_from_project(jira_project, role_id, jira_user_id):
    returnMsg = {
        'success': False,
        'msg': ''
    }
    headers = {
        'Authorization': 'Basic {token}'.format(token=pms_settings.JIRA_HOST_TOKEN["Token"])
    }
    proxies = pms_settings.PROXIES
    path = '{jira_host}{api_path}'.format(jira_host=pms_settings.JIRA_HOST_TOKEN["Host"],
        api_path=pms_settings.JIRA_HOST_TOKEN["RemoveUserFromProjectRole"].format(projectIdOrKey = jira_project, projectRoleId = role_id, userId=jira_user_id))

    try:
        requests.packages.urllib3.disable_warnings()
        r = requests.delete(
            path,
            verify=False,
            proxies=proxies,
            headers=headers
        )
        
        if r.status_code == 204:
            returnMsg['success'] = True
            returnMsg['msg'] = ''
        else:
            returnMsg['success'] = False
            returnMsg['msg'] = 'Delete User from Project failed, Status code: {statusCode}, message: {message}'.format(statusCode=r.status_code, message=r.json())
    except Exception as e:
        print(e)
        returnMsg['success'] = False
        returnMsg['msg'] = 'Call Jira API Error: {}'.format(e)  

    return returnMsg     

def checkRepo(versionControl, repoId, url, utJobName):
    result = {
        'repoMsg': None,
        'repoCoverage': None,
        'findRepo': False
    }
    if utJobName is not None and utJobName != '':
        # 檢查Repo
        if versionControl == 'GitLab':
            if url is None and url == '':
                # print('Repo URL為空!')            
                result['repoMsg'] = 'Repo URL is Empty!'.format()
            else:
                # print(pms_settings.GITLAB_HOST_TOKEN)
                parsed_uri = urlparse(url)
                # print(parsed_uri)
                for git in pms_settings.GITLAB_HOST_TOKEN:
                    # print(git)
                    if parsed_uri.netloc == git['Host']:
                        result['findRepo'] = True
                        # print(git['Token'])
                        headers = {'Authorization': 'Bearer {}'.format(git['Token'])}
                        try: 
                            requests.packages.urllib3.disable_warnings()
                            r = requests.get(
                                'https://{Host}/api/v4/projects/{RepoId}/jobs'.format(Host = git['Host'], RepoId = repoId),
                                verify=False,
                                headers=headers)
                            if r.status_code == 200:
                                # print(r.json())
                                jobs = r.json()
                                foundUTJob = False
                                for job in jobs:
                                    # print(job['name'])
                                    if job['name'] == utJobName:
                                        foundUTJob = True
                                        result['repoCoverage'] = job['coverage']
                                        break
                                if foundUTJob is not True:
                                    result['repoMsg'] = 'Cannot find UT Job: {}, please check!'.format(utJobName)
                                else:
                                    if result['repoCoverage'] is None:
                                        result['repoMsg'] = 'Cannot get Coverage, please check!'
                                    else:
                                        result['repoMsg'] = 'Get UT Coverage successfully!'
                            else:
                                # 找不到PROJECT或是沒有權限
                                # print(r.json())
                                result['repoMsg'] = 'Cannot find project in Gitlab or no permission.'

                        except Exception as e:
                            # print(e)
                            result['repoMsg'] = 'Get Gitlab Error: {}'.format(e)
                        break 
            if result['findRepo'] is False:
                result['repoMsg'] = 'Cannot find this gitlab Host: {}'.format(parsed_uri.netloc)
    # print(result)
    return result
