"""DjangoAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authtoken.views import obtain_auth_token

from rest_framework.routers import DefaultRouter

# from rest_framework.documentation import include_docs_urls
from imp_bo.views import ImpBoViewSet
from imp_bg.views import ImpBgViewSet
from imp_bu.views import ImpBuViewSet
from imp_div.views import ImpDivViewSet
from imp_dept.views import ImpDeptViewSet
from imp_cal.views import ImpCalViewSet
from imp_projcategory.views import ProjCategoryViewSet
from imp_projtype.views import ProjTypeViewSet
from imp_resource.views import ResourceViewSet
from imp_extnames.views import ExtnamesViewSet
from imp_ib.views import ImpIbViewSet
from imp_ibln.views import ImpIblnViewSet
from imp_pajln.views import PajlnViewSet
from imp_pajmonth.views import PajMonthViewSet
from imp_pajtxt.views import PajTxtViewSet
from imp_prf.views import PrfViewSet
from imp_prfln.views import ImpPrflnViewSet
from imp_budln.views import ImpBudlnViewSet
from imp_bud.views import ImpBudViewSet
from imp_tss.views import ImpTssViewSet
from imp_tsspast.views import ImpTssPastViewSet
from pms_jira_project_role.views import PmsJiraProjectRoleViewSet
from pms_jira_it_user.views import PmsJiraITUserViewSet
from uploader import views
from pms_project.views import PmsProjectViewSet
from pms_project_log.views import PmsProjectLogViewSet
from pms_jira_user.views import PmsJiraUserViewSet
from pms_jira_user_group.views import PmsJiraUserGroupViewSet
from pms_project_user.views import PmsProjectUserViewSet
from pms_project_version_control.views import PmsProjectVersionControlViewSet
from pms_sign.views import PmsSignViewSet, PmsSignExternalViewSet
from pms_common.views import PmsCommonViewSet
from v_pms_register_jira_user.views import VPmsRegisterJiraUserViewSet
from v_pms_delete_jira_user.views import VPmsDeleteJiraUserViewSet
from v_pms_user_in_jira.views import VPmsUserInJiraViewSet

# from rest_framework_swagger.views import get_swagger_view

router = DefaultRouter(trailing_slash=False)
router.register("bo", ImpBoViewSet, basename="bo")
router.register("bg", ImpBgViewSet, basename="bg")
router.register("bu", ImpBuViewSet, basename="bu")
router.register("div", ImpDivViewSet, basename="div")
router.register("dept", ImpDeptViewSet, basename="dept")
router.register("cal", ImpCalViewSet, basename="cal")
router.register("ib", ImpIbViewSet, basename="ib")
router.register("ibln", ImpIblnViewSet, basename="ibln")
router.register("proj_category", ProjCategoryViewSet, basename="proj_category")
router.register("proj_type", ProjTypeViewSet, basename="proj_type")
router.register("resource", ResourceViewSet, basename="resource")
router.register("extnames", ExtnamesViewSet, basename="extnames")
router.register("pajln", PajlnViewSet, basename="pajln")
router.register("paj_month", PajMonthViewSet, basename="paj_month")
router.register("paj_txt", PajTxtViewSet, basename="paj_txt")
router.register("prf", PrfViewSet, basename="prf")
router.register("prfln", ImpPrflnViewSet, basename="prfln")
router.register("bud", ImpBudViewSet, basename="bud")
router.register("budln", ImpBudlnViewSet, basename="budln")
router.register("tss", ImpTssViewSet, basename="tss")
router.register("tss_past", ImpTssPastViewSet, basename="tss_past")
# router.register("uploader", views.as_view(), basename="uploader")
router.register("pms_project", PmsProjectViewSet, basename="pms_project")
router.register("pms_project_log", PmsProjectLogViewSet, basename="pms_project_log")
router.register("pms_Jira_User", PmsJiraUserViewSet, basename="pms_jira_user")
router.register("pms_Jira_User_group", PmsJiraUserGroupViewSet, basename="pms_jira_user_group")
router.register("pms_project_version_control", PmsProjectVersionControlViewSet, basename="pms_project_version_control")
router.register("pms_project_user", PmsProjectUserViewSet, basename="pms_project_user")
router.register("pms_jira_project_role", PmsJiraProjectRoleViewSet, basename="pms_jira_project_role")
router.register("pms_jira_it_user", PmsJiraITUserViewSet, basename="pms_jira_it_user")
router.register("pms_sign", PmsSignViewSet, basename="pms_sign")
router.register("pms_sign_external", PmsSignExternalViewSet, basename="pms_sign_external")
router.register("v_pms_register_jira_user", VPmsRegisterJiraUserViewSet, basename="v_pms_register_jira_user")
router.register("v_pms_delete_jira_user", VPmsDeleteJiraUserViewSet, basename="v_pms_delete_jira_user")
router.register("v_pms_user_in_jira", VPmsUserInJiraViewSet, basename="v_pms_user_in_jira")

schema_view = get_schema_view(
    openapi.Info(
        title="IMP API",
        default_version="v1.0",
        description="IMP API",
        terms_of_service="https://portal.wistron.com/",
        # contact=openapi.Contact(email="Rick_Wu@wistron.com"),
        # license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("accounts/", admin.site.urls),
    path("api/", include((router.urls, "api"), namespace="api")),
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("api/uploader/", include("uploader.urls", namespace="uploader")),
    path("api/api-token-auth/", obtain_auth_token, name="api_token_auth"),
    # path(
    #     "api/docs/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    # ),
]
