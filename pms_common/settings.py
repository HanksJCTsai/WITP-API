
class pms_settings():
    GITLAB_HOST_TOKEN = [
        {
            "Host": "gitlab.wistron.com",
            "Token": "p2fcoDehufVdMsyJUPuH"
        }
    ]

    JIRA_HOST_TOKEN = {
        "Host": "https://swpc.atlassian.net",
        "UserId": "Scott_Yang@wistron.com",
        "Token": "U2NvdHRfWWFuZ0B3aXN0cm9uLmNvbTpZeHJxbVBFdkx4RGFvN0hoUnV2SzJGNDg=",
        "CreateProject": "/rest/api/3/project",
        "ValidateJiraKey": "/rest/api/3/projectvalidate/key?key={jiraKey}",
        "GetProjectRole": "/rest/api/2/project/{projectIdOrKey}/role",
        "GetProjectRoleByID": "/rest/api/2/project/{projectIdOrKey}/role/{projectRoleId}",
        "AssignUserIntoProjectRole": "/rest/api/3/project/{projectIdOrKey}/role/{projectRoleId}",
        "RemoveUserFromProjectRole": "/rest/api/3/project/{projectIdOrKey}/role/{projectRoleId}?user={userId}"
    }

    JIRA_PROJECT_ADMIN = {
        "AdminProjectRole": "Administrator",
        "AdminUserList": [
            {
                "Name": "Scott Yang",
                "JiraId": "70121:a8170350-5141-425e-ba2f-feeab4335089"
            },
            {
                "Name": "Bruce CH Chang",
                "JiraId": "5f7d7a0fe31b69006fcff2df"
            }
        ]
    }

    JIRA_PROJECT_DEFAULT_ROLE = {
        "ProjectRole": [
            "Member"
        ]
    }

    JIRA_PROJECT_SKIP_ROLE = {
        "ProjectRole": [
            "atlassian-addons-project-access"
        ]
    }

    PROXIES = {
    'http': 'http://whqproxys.wistron.com:8080',
    'https': 'http://whqproxys.wistron.com:8080',
    }

    WISTRON_PORTAL = {
        "SERVICEID": "IMPPMSQAS",
        "AUTHORIZATIONCODE": "CRkBSBFN",
        "FORMTYPE": "JIRAAPPLICATION",
        "APIHOST": "https://portalapp-qas.wistron.com",
        "InsertApprovalForm": "/api/AP/InsertApprovalForm",
        "CancelApprovalForm": "/api/AP/CancelApprovalForm"
    }