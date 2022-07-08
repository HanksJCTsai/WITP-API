from datetime import datetime
from tkinter import W
from certifi import contents
from django.db import connection
from rest_framework import viewsets
from pms_project.models import PmsProject, PmsProjectLog
from pms_project_user.models import PmsProjectUserLog
from .models import PmsSign, PmsSignContent, PmsSignDetail, PmsSignId
from .serializers import PmsSignSerializer
from pms_common.views import PmsCommonViewSet, PlainTextParser
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from django.db.models.functions import Upper
from django.db import transaction
from dateutil import parser
from pms_project.views import PmsProjectViewSet
from django.conf import settings
from django.contrib.auth.models import User
from pms_common.settings import pms_settings
import json
import xml.etree.ElementTree as ET

id = openapi.Parameter('id', in_=openapi.IN_QUERY,
                           type=openapi.TYPE_NUMBER, description='ID', required=True,)
projectId = openapi.Parameter('projectId', in_=openapi.IN_QUERY,
                           type=openapi.TYPE_NUMBER, description='Project ID', required=True,)
email = openapi.Parameter('email', in_=openapi.IN_QUERY,
                           type=openapi.TYPE_STRING, description='Email', required=True,)
signId = openapi.Parameter('signId', in_=openapi.IN_QUERY,
                           type=openapi.TYPE_STRING, description='Sign ID', required=False,)
result = openapi.Parameter('result', in_=openapi.IN_QUERY,
                           type=openapi.TYPE_STRING, description='Result', required=False,)
startDate = openapi.Parameter('startDate', in_=openapi.IN_QUERY,
                           type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Start Date', required=False,)
endDate = openapi.Parameter('endDate', in_=openapi.IN_QUERY,
                           type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='End Date', required=False,)

# Create your views here.        
class PmsSignViewSet(viewsets.ModelViewSet):
    serializer_class = PmsSignSerializer
    queryset = PmsSign.objects.filter()
    
    def get_queryset(self):
        queryset = PmsSign.objects.all().annotate(pms_sign_detail_pms_sign_head_id_fkey__sign_user_email_upper=Upper('pms_sign_detail_pms_sign_head_id_fkey__sign_user_email'))
        email = self.request.query_params.get('email')
        signId = self.request.query_params.get('signId')
        result = self.request.query_params.get('result')
        startDate = self.request.query_params.get('startDate')
        endDate = self.request.query_params.get('endDate')        
        
        if email is not None:
            queryset = queryset.filter(pms_sign_detail_pms_sign_head_id_fkey__sign_user_email_upper=email.upper())        
        if signId is not None:
            queryset = queryset.filter(sign_id__icontains=signId.upper())     
        if result is not None:
            if result == 'OPEN':
                queryset = queryset.filter(result=None)
            else:
                queryset = queryset.filter(result=result)        
        if startDate is not None:     
            startDateFormat = parser.parse('{startDate} 00:00:00'.format(startDate = startDate))
            queryset = queryset.filter(create_date__gte=startDateFormat)
        if endDate is not None:
            endDateFormat = parser.parse('{endDate} 23:59:59'.format(endDate = endDate))
            queryset = queryset.filter(create_date__lte=endDateFormat)           

        return queryset

    @swagger_auto_schema(
        operation_summary='Get Project Sign List',
        manual_parameters=[email, signId, result, startDate, endDate],
    )
    def list(self, request, *args, **kwargs):
        try:            
            queryset = self.get_queryset()
            data = namedtuplefetchall(queryset)
            result = {
                "success": True,
                "msg": "",
                "data": data
            }
            return Response(result)
        
        except Exception as e:
            result = {
                "success": False,
                "msg": e.args[0],
            }
            return Response(result)

    @swagger_auto_schema(
        operation_summary='Send project to sign',
        manual_parameters=[projectId],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'remark': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Remark',
                )
            },
        ),
    )
    @action(detail=False, methods=["post"])
    def send_to_sign(self, request, pk=None):
        try:
            with transaction.atomic(): 
                projectId = self.request.query_params.get('projectId')
                project = PmsProject.objects.filter(id=projectId)
                remark = request.data.get('remark')
                updateUser = PmsProjectUserLog.objects.filter(project_id=projectId).filter(approved=False).order_by('trn_date')

                if len(updateUser) > 0:
                    # 專案人員異動，需要簽核
                    # 簽核                
                    maxSeq = PmsSignViewSet.calculateSignId()
                    signHead = PmsSign.objects.create(
                        sign_id = "{date}{seq}".format(date=datetime.now().strftime('%Y%m%d'), seq=str(maxSeq).zfill(3)),
                        project_id = project.first().id,
                        requester_remark = remark,
                    )
                    signDetail = signHead.pms_sign_detail_pms_sign_head_id_fkey.create(
                        seq = 1,
                        # division = project.division,
                        # sign_user = project.division_supervisor,
                        # sign_user_email = project.division_supervisor_email,
                        division = 'MLD000',
                        sign_user = 'Scott Yang',
                        sign_user_employee_id = '10309100',
                        sign_user_email = 'SCOTT_YANG@WISTRON.COM',
                    )
                    project_content = PmsProjectViewSet.getProjectDetail(project)
                    update_user = renderUpdateUser(updateUser)
                    signContent = PmsSignContent.objects.create(
                        sign = signHead,
                        project_content = project_content,
                        update_user = update_user
                    )
                    project.update(status=1)

                    vc_body = []
                    vc_html = ''
                    for value in project.first().pms_prj_version_control_project_id_fkey.all():   
                        vc_body.append(
                            PmsCommonViewSet.renderVCBody(value.version_control, value.type, value.repo_id,
                            value.repo_url, value.ut_job_name, '', '', '')
                        )
                    if len(vc_body) > 0:
                        vc_html = PmsCommonViewSet.renderVCMailContent(vc_body)

                    user_body = []
                    user_html = ''
                    for value in project.first().pms_prj_user_project_id_fkey.filter(deleted=False):
                        userData = value.user
                        user_body.append(
                            PmsCommonViewSet.renderUserBody(value.user.user_name, value.user.employee_id, value.user.email,
                                value.project_role, value.jira_role, '')
                            )
                    if len(user_body) > 0:
                        user_html = PmsCommonViewSet.renderUserMailContent(user_body)

                    update_user_body = []
                    update_user_html = ''
                    for value in update_user:
                        update_user_body.append(
                            PmsCommonViewSet.renderUserBody(value['user_name'], value['employee_id'], value['email'],
                                value['project_role'], value['jira_role'], value['action'])
                            )
                    if len(update_user_body) > 0:
                        update_user_html = PmsCommonViewSet.renderUserMailContent(update_user_body)

                    projectLog = PmsProjectLog.objects.filter(project_id = project.first().id).order_by('trn_date').first()

                    project_detail = PmsCommonViewSet.renderProjectBody(project.first(), projectLog.trn_user)

                    # 電子郵件內容樣板
                    email_template = PmsCommonViewSet.renderMailContent(
                        template = 'sign',
                        userName = signDetail.sign_user,
                        projectDetail = project_detail,
                        vcBody = vc_html,
                        userBody = user_html,
                        updateUserBody = update_user_html,
                        projectName = project.first().project_name,
                        signId = signHead.sign_id,
                        remark = signHead.requester_remark,
                    )

                    auth_user = User.objects.get(username=project.first().create_user)
                    PmsCommonViewSet.sendEmail(
                        '[IMP] Jira Account Application waiting for your approval: by {ProjectName}-{Division}-{User}'
                            .format(ProjectName = project.first().project_name, Division = project.first().division, User = auth_user.username),
                        email_template,
                        [signDetail.sign_user_email],
                        settings.PMS_EMAIL_CC
                    )

                    
                    approve_to_wistron_portal = PmsCommonViewSet.renderApproveXMLBody(project.first(), signHead, signDetail, vc_body, user_body, update_user_body)
                    mcp_result = send_to_mcp(approve_to_wistron_portal)
                    if mcp_result['success'] == True:
                        print(mcp_result['mcp_id'])
                        signHead.mcp_id = mcp_result['mcp_id']
                        signHead.save()
                    else:
                        raise Exception(mcp_result['msg'])

                else:
                    # 專案人員沒有異動，不需要簽核
                    project.update(status=4)

            result = {
                "success": True,
                "msg": "",
            }

            return Response(result)
        except Exception as e:
            print(e)
            result = {
                "success": False,
                "msg": e.args[0],
            }
            return Response(result)

    @swagger_auto_schema(
        operation_summary='Sign',
        manual_parameters=[id, email],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'result': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Result',
                ),
                'remark': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Remark',
                )
            },
        ),
    )
    @action(detail=False, methods=["post"])
    def confirm_sign(self, request, pk=None):
        try:
            id = self.request.query_params.get('id')
            email = self.request.query_params.get('email')
            sign = PmsSign.objects.get(id=id)
            sign_result = request.data.get('result')
            remark = request.data.get('remark')
            signDetail = sign.pms_sign_detail_pms_sign_head_id_fkey.all().annotate(sign_user_email_upper=Upper('sign_user_email')).get(sign_user_email_upper=email.upper())

            confirm_sign(sign.sign_id, signDetail.seq, sign_result, remark, True)

            result = {
                "success": True,
                "msg": "",
            }

            return Response(result)
        except Exception as e:
            result = {
                "success": False,
                "msg": e.args[0],
            }
            return Response(result)

    def calculateSignId():
        pmsSignId = PmsSignId.objects.all()
        maxSeq = 1
        if len(pmsSignId) > 0:
            currentSeq = pmsSignId.get(id=1)
            if datetime.now().strftime('%Y%m%d') <= currentSeq.create_date.strftime("%Y%m%d"):
                maxSeq = currentSeq.sign_id + 1
            currentSeq.sign_id = maxSeq
            currentSeq.create_date = datetime.now()
            currentSeq.save()
        else:
            currentSeq = PmsSignId.objects.create(
                sign_id = maxSeq,
                create_date = datetime.now(),
            )
        return maxSeq

def namedtuplefetchall(queryset):
    result = [
        {
            "id": r.id,
            "sign_id": r.sign_id,
            "result": r.result,
            "requester_remark": r.requester_remark,
            "create_date": r.create_date.strftime("%Y/%m/%d %H:%M:%S") if r.create_date else None,
            "signed_date": r.signed_date.strftime("%Y/%m/%d %H:%M:%S") if r.signed_date else None,
            "project": r.pmssigncontent.project_content if r.pmssigncontent else [],
            "update_users": r.pmssigncontent.update_user if r.pmssigncontent else [],
            "mcp_id": r.mcp_id,
            "sign_detail": [
                {
                    "detail_id": s.id,
                    "detail_seq": s.seq,
                    "sign_user": s.sign_user,
                    "sign_user_employee_id": s.sign_user_employee_id,
                    "sign_user_email": s.sign_user_email,
                    "result": s.result,
                    "remark": s.remark,
                    "signed_date": r.signed_date.strftime("%Y/%m/%d %H:%M:%S") if r.signed_date else None,
                }
                for s in r.pms_sign_detail_pms_sign_head_id_fkey.all()
            ], 
        }
        for r in queryset
    ]
    return result

def renderUpdateUser(updateUser):
    result = [
        {
            "id": q.id,
            "project_id": q.project_id,
            "user_id": q.user_id,
            "user_name": q.user_name,
            "employee_id": q.employee_id,
            "email": q.email,
            "project_role": q.project_role,
            "jira_role": q.jira_role,
            "join_date": q.join_date.strftime("%Y/%m/%d") if q.join_date else None,
            "action": q.action,
            "trn_date": q.trn_date.strftime("%Y/%m/%d %H:%M:%S") if q.trn_date else None,
            "trn_user": q.trn_user,
        }
        for q in updateUser
    ]
    return result

def send_to_mcp(body):   
    returnMsg = {
        'success': False,
        'msg': '',
        'mcp_id': None,
    }

    headers = {
        'Accept': '*/*',
        'Content-Type': 'text/plain'
    }

    try: 
        path = '{mcp_host}{api_path}'.format(mcp_host=pms_settings.WISTRON_PORTAL["APIHOST"],
            api_path=pms_settings.WISTRON_PORTAL["InsertApprovalForm"])

        payload = body.encode()

        response = PmsCommonViewSet.post_external_api(path, headers, payload)

        if response['success'] == True:   
            if response['response'].json()['rtnCode'] == 1:
                returnMsg['success'] = True
                returnMsg['msg'] = ''
                returnMsg['mcp_id'] = response['response'].json()['data']
            else:
                returnMsg['success'] = False
                returnMsg['msg'] = response[response].json()['rtnMsg']
        else:
            raise Exception(response['msg'])

                        
    except Exception as e:
        print(e)
        returnMsg['success'] = False
        returnMsg['msg'] = 'send_to_mcp Error: {}'.format(e)

    return returnMsg

def cancel_to_mcp(mcp_id):   
    returnMsg = {
        'success': False,
        'msg': '',
        'mcp_id': None,
    }

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    try: 
        path = '{mcp_host}{api_path}'.format(mcp_host=pms_settings.WISTRON_PORTAL["APIHOST"],
            api_path=pms_settings.WISTRON_PORTAL["CancelApprovalForm"])

        payload = {
            "serviceID": pms_settings.WISTRON_PORTAL["SERVICEID"],
            "authCode": pms_settings.WISTRON_PORTAL["AUTHORIZATIONCODE"],
            "MessageID": str(mcp_id)   
        }

        response = PmsCommonViewSet.post_external_api(path, headers, json.dumps(payload))

        if response['success'] == True:   
            if response['response'].json()['rtnCode'] == 1:
                returnMsg['success'] = True
                returnMsg['msg'] = ''
                returnMsg['mcp_id'] = response['response'].json()['data']
            else:
                returnMsg['success'] = False
                returnMsg['msg'] = response[response].json()['rtnMsg']
        else:
            raise Exception(response['msg'])

                        
    except Exception as e:
        print(e)
        returnMsg['success'] = False
        returnMsg['msg'] = 'send_to_mcp Error: {}'.format(e)

    return returnMsg

def confirm_sign(sign_id, sign_seq, result, remark, cancel_mcp):
    try:
        with transaction.atomic(): 
            print(sign_id, sign_seq, result, remark, cancel_mcp)
            # 簽核
            sign = PmsSign.objects.get(sign_id = sign_id)
            print(sign.sign_id)
            project = PmsProject.objects.get(id=sign.project_id)
            signDetail = sign.pms_sign_detail_pms_sign_head_id_fkey.all().get(seq=sign_seq)
            print(signDetail.seq)
            signDetail.result = result
            signDetail.remark = remark
            signDetail.signed_date = datetime.now()
            signDetail.save()

            rejectDetail = sign.pms_sign_detail_pms_sign_head_id_fkey.all().filter(result='REJECTED')
            # 只要有一筆拒絕，則整筆都拒絕
            if len(rejectDetail)>0:
                sign.result = 'REJECTED'
                sign.signed_date = datetime.now()
                sign.save()
                project.status=3
                project.save()

                sign_list = sign.pms_sign_detail_pms_sign_head_id_fkey.all()
                sign_html = PmsCommonViewSet.renderSignContent(sign_list)
                auth_user = User.objects.get(username=project.create_user)
                email_template = PmsCommonViewSet.renderMailContent(
                    template = 'sign_reject',
                    userName = auth_user.username,
                    projectName = project.project_name,
                    signId = sign.sign_id,
                    remark = sign.requester_remark,
                     signDetail = sign_html
                 )
                PmsCommonViewSet.sendEmail(                        
                    '[IMP] {ProjectName} Jira Account Application rejected: by {signer}-{Division}'
                        .format(ProjectName = project.project_name, signer = rejectDetail.first().sign_user, Division = project.division),
                    email_template,
                    [auth_user.email],
                    settings.PMS_EMAIL_CC
                )
                # 簽核通過，須向MCP發送取消簽核
                if cancel_mcp == True:
                    cancel_to_mcp(sign.mcp_id)
            else:
                # 只要有一筆還OPEN，則整筆都OPEN!
                waitDetail = sign.pms_sign_detail_pms_sign_head_id_fkey.all().filter(result=None)                    
                if len(waitDetail)<=0:
                    sign.result = 'APPROVED'
                    sign.signed_date = datetime.now()
                    sign.save()
                    project.status=4
                    project.save()

                    PmsProjectUserLog.objects.filter(project_id=sign.project_id).filter(approved=False).update(approved=True)
                    sign_list = sign.pms_sign_detail_pms_sign_head_id_fkey.all()
                    sign_html = PmsCommonViewSet.renderSignContent(sign_list)
                    auth_user = User.objects.get(username=project.create_user)
                    email_template = PmsCommonViewSet.renderMailContent(
                        template = 'sign_approve',
                        userName = auth_user.username,
                        projectName = project.project_name,
                        signId = sign.sign_id,
                        remark = sign.requester_remark,
                        signDetail = sign_html
                    )
                    PmsCommonViewSet.sendEmail(                    
                        '[IMP] {ProjectName} Jira Account Application Approved'.format(ProjectName = project.project_name),
                        email_template,
                        [auth_user.email],
                        settings.PMS_EMAIL_CC
                    )

                    # 簽核通過，須向MCP發送取消簽核
                    if cancel_mcp == True:
                        cancel_to_mcp(sign.mcp_id)
                else:
                    sign.result = None
                    sign.signed_date = None
                    sign.save()
                    project.status=1
                    project.save()

    except Exception as e:
        raise Exception(e)


class PmsSignExternalViewSet(viewsets.ModelViewSet):
    serializer_class = PmsSignSerializer
    parser_classes = [PlainTextParser]
    queryset = PmsSignDetail.objects.all()
    
    @swagger_auto_schema(
        operation_summary='Receive Result from MCP',
        manual_parameters=[],
        contents='application/xml',
    )
    @action(detail=False, methods=["post"])
    def receive_result_from_mcp(self, request, pk=None):
        try:
            # print(request.data)
            root = ET.fromstring(request.data)
            form_id =  root[2].find('FORMID').text
            sign_id = form_id.split('-')[0]
            sign_seq = form_id.split('-')[1]
            sign_result = ''
            if root[2].find('CHKRESULT').text == 'Approve':
                sign_result = 'APPROVED'
            else:
                sign_result = 'REJECTED'
            remark = root[2].find('APPRSUMMARY').text

            confirm_sign(sign_id, sign_seq, sign_result, remark, False)

            result = {
                    "rtnCode": 1,
                    "rtnMsg": "",
                }
            return Response(result)
        except Exception as e:
            result = {
                    "rtnCode": 0,
                    "rtnMsg": e.args[0],
                }
            # print(result)
            return Response(result)
