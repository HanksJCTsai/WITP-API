from rest_framework import viewsets
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from pms_common.settings import pms_settings
import requests
from rest_framework.parsers import BaseParser

# Create your views here.
class PmsCommonViewSet(viewsets.ModelViewSet):

    def sendEmail(subject, mailBody, mailTo, mailCC):
        email = EmailMessage(
            subject,  # 電子郵件標題
            mailBody,  # 電子郵件內容
            settings.EMAIL_HOST_USER,  # 寄件者
            mailTo,  # 收件者
            None,
            None,
            None,
            None,
            mailCC
        )

        email.content_subtype = 'html'
        email.fail_silently = False
        email.encoding = 'UTF-8'
        email.send()

    # region 產生各種Mail Body
    def renderProjectBody(project, trnUser):

        product_type = None
        if 'Product' in project.product_type:
            product_type = '{product_type} / 產品'.format(product_type=product_type) if product_type else '產品'
        if 'Model' in project.product_type:
            product_type = '{product_type} / 模型'.format(product_type=product_type) if product_type else '模型'
        
        mode = None
        
        if project.mode == 'agile':
            mode = '敏捷式開發'
        elif project.mode == 'waterfall':
            mode = '瀑布式開發'
        elif project.mode == 'kanban':
            mode = '看板'

        result = render_to_string(
            'projects/project_table.html',
            {
                'project_id': project.id,
                'project_name': project.project_name,
                'project_code': project.project_code,
                'division': project.division,
                'division_supervisor': project.division_supervisor,
                'division_supervisor_email': project.division_supervisor_email,
                'mode': mode,
                'product_type': product_type,
                'plan_start': project.plan_start,
                'plan_end': project.plan_end,
                'jira_key': project.jira_key,
                'jira_name': project.jira_name,
                'user_contact': project.user_contact.user_name,
                'user_contact_email': project.user_contact.email,
                'it_contact': project.it_contact.user_name,
                'it_contact_email': project.it_contact.email,
                'status': project.status,
                'involve_pms': project.involve_pms,
                'involve_pms_start': project.involve_pms_start,
                'involve_pms_end': project.involve_pms_end,
                'create_date': project.create_date,
                'close': project.close,
                'close_date': project.close_date,
                'approve_date': project.approve_date,
                'trn_user': trnUser,
            }
        )
        # print(result)
        return result

    def renderVCBody(versionControl, type, repoId, repoUrl, utJobName, repoMsg, repoCoverage, action):
        return {
            'version_control': versionControl,
            'version_control_type': type,
            'repo_id': repoId,
            'repo_url': repoUrl,
            'ut_job_name': utJobName,
            'gitlab_message': repoMsg,
            'gitlab_coverage': repoCoverage,
            'operation': action,
        }

    def renderVCMailContent(vc_body):
        restult =  render_to_string(
            'projects/version_control_table.html',
            {
                'vc_list': vc_body,
            }
        )
        # print(restult)
        return  restult

    def renderUserBody(userName, employeeId, email, projectRole, jiraRole, action):
        return {
            'user_name': userName,
            'employee_id': employeeId,
            'email': email,
            'project_role': projectRole,
            'jira_role': jiraRole,
            'operation': action,
        }

    def renderUserMailContent(user_body):
        result = render_to_string(
            'projects/project_user_table.html',
            {
                'user_list': user_body,
            }
        )
        # print(result)
        return  result

    def renderSignContent(sign_list):
        result = render_to_string(
            'sign/sign_table.html',
            {
                'sign_list': sign_list,
            }
        )
        # print(result)
        return  result

    def renderMailContent(template, userName = '', projectDetail = '', vcBody = '', 
        userBody = '', jiraKey = '', remark = '', data=[], updateUserBody = '',
        projectName = '', signDetail = '', signId = ''):
        result = ''
        if template == 'add_project_success_to_tl':
            result = render_to_string(
                'projects/add_project_success_to_tl.html',
                {
                    'username': userName,
                    'project_detail': projectDetail,
                    'vc_detail': vcBody,
                    'user_detail': userBody,
                    'impurl': settings.IMP_URL
                }
            )
        elif template == 'update_project_success_to_tl':
            result = render_to_string(
                'projects/update_project_success_to_tl.html',
                {
                    'username': userName,
                    'project_detail': projectDetail,
                    'vc_detail': vcBody,
                    'user_detail': userBody,
                    'impurl': settings.IMP_URL
                }
            )
        elif template == 'create_jira_success_to_tl':
            result = render_to_string(
                'projects/create_jira_success_to_tl.html',
                {
                    'username': userName,
                    'jira_key': jiraKey,
                    'remark': remark,
                    'impurl': settings.IMP_URL,
                    'add_user_result': data[0],
                    'delete_user_result': data[1],
                }
            )
        elif template == 'create_jira_failed_to_tl':
            result = render_to_string(
                'projects/create_jira_failed_to_tl.html',
                {
                    'username': userName,
                    'jira_key': jiraKey,
                    'remark': remark,
                    'impurl': settings.IMP_URL
                }
            )
        elif template == 'sign':
            result = render_to_string(
                'sign/sign.html',
                {
                    'signer': userName,
                    'project_name': projectName,
                    'sign_id': signId,
                    'remark': remark,
                    'project_detail': projectDetail,
                    'vc_detail': vcBody,
                    'user_detail': userBody,
                    'update_user_detail': updateUserBody,
                    'impurl': settings.IMP_URL
                }
            )
        elif template == 'sign_reject':
            result = render_to_string(
                'sign/sign_reject.html',
                {
                    'user_name': userName,
                    'project_name': projectName,
                    'sign_id': signId,
                    'remark': remark,
                    'sign_result': signDetail,
                    'update_user_detail': updateUserBody,
                    'impurl': settings.IMP_URL
                }
            )
        elif template == 'sign_approve':
            result = render_to_string(
                'sign/sign_approve.html',
                {
                    'user_name': userName,
                    'project_name': projectName,
                    'sign_id': signId,
                    'remark': remark,
                    'sign_result': signDetail,
                    'update_user_detail': updateUserBody,
                    'impurl': settings.IMP_URL
                }
            )

        # print(result)
        return  result
    
    #endregion

    #region 產生XML Body
    def renderApproveXMLBody(project, sign, signDetail, versionControls, users, updateUsers):

        project.product_type = renderProductType(project.product_type, 'zh-TW')
        project.mode = renderMode(project.mode, 'zh-TW')

        restult =  render_to_string(
            'sign/portal_approve_body.xml',
            {
                'SERVICEID': pms_settings.WISTRON_PORTAL['SERVICEID'],
                'AUTHORIZATIONCODE': pms_settings.WISTRON_PORTAL['AUTHORIZATIONCODE'],
                'DATACREATEDTIME': 20211104130017,
                'FORMTYPE': pms_settings.WISTRON_PORTAL['FORMTYPE'],
                'USERID': signDetail.sign_user_employee_id,
                'SIGNSEQ': signDetail.seq,
                'PROJECT': project,
                'SIGN': sign,
                'VCLIST': versionControls,
                'USERLIST': users,
                'USERCOUNT': len(users),
                'UPDATEUSERLIST': updateUsers,
                'ADDUSERCOUNT': len([user for user in updateUsers if user['operation'] == 'ADD']),
                'DELETEUSERCOUNT': len([user for user in updateUsers if user['operation'] == 'DELETED']),
                'UPDATEUSERCOUNT': len([user for user in updateUsers if user['operation'] == 'UPDATE']),
            }
        )
        # print(restult)
        return  restult
    #endregion

    #region Call External API
    def post_external_api(uri, headers, payload):
        returnMsg = {
            'success': False,
            'msg': '',
            'response': None
        }
            
        proxies = pms_settings.PROXIES

        try:
            requests.packages.urllib3.disable_warnings()
            r = requests.post(
                uri,
                verify=False,
                proxies=proxies,
                headers=headers,
                data=payload
            )

            returnMsg['success'] = True
            returnMsg['msg'] = ''
            returnMsg['response'] = r
                        
        except Exception as e:
            print(e)
            returnMsg['success'] = False
            returnMsg['msg'] = 'Call API Error: {}'.format(e)

        return returnMsg
    #endregion

def renderProductType(product_type, language):
    result = None
        
    if language == 'zh-TW':
        if 'Product' in product_type:
            result = '{product_type} / 產品'.format(product_type=result) if result else '產品'
        if 'Model' in product_type:
            result = '{product_type} / 模型'.format(product_type=result) if result else '模型'
    elif language == 'en-US':
        if 'Product' in product_type:
            result = '{product_type} / Product'.format(product_type=result) if result else 'Product'
        if 'Model' in product_type:
            result = '{product_type} / Model'.format(product_type=result) if result else 'Model'

    return result

def renderMode(mode, language):
    result = None
        
    if language == 'zh-TW':
        if mode == 'agile':
            result = '敏捷式開發'
        elif mode == 'waterfall':
            result = '瀑布式開發'
        elif mode == 'kanban':
            result = '看板'
    elif language == 'en-US':
        if mode == 'agile':
            result = 'Agile'
        elif mode == 'waterfall':
            result = 'Waterfall'
        elif mode == 'kanban':
            result = 'Kanban'

    return result

class PlainTextParser(BaseParser):
    """
    Plain text parser.
    """
    media_type = 'text/plain'

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Simply return a string representing the body of the request.
        """
        return stream.read()
