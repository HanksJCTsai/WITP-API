from django.db import connection
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from collections import namedtuple

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .models import ImpBud
from .serializers import ImpBudSerializer

# Create your views here.


class ImpBudViewSet(viewsets.ModelViewSet):
    serializer_class = ImpBudSerializer
    queryset = ImpBud.objects.filter()

    def get_permissions(self):
        # 決定哪些method需要哪些認證
        # GET不用
        if self.request.method in ["POST","PUT","PATCH","DELETE"]:
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.AllowAny()]

    @swagger_auto_schema(
        method='post',
        operation_summary="Query budget projectn by Id",
        operation_description="Query budget project by Id",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id": openapi.Schema(type=openapi.TYPE_STRING, description="Budget budget id"),
            }
        ),
    )
    @action(detail=False, methods=["post"])
    def quer_bud_id(self, request, pk=None):
        sqlParameters = []
        req = request.data
        bud_id = req.get("id")
        COMMON_QUERY = """SELECT BUD.id, BUD.project_year, BUD.project_name, BUD.it_pm, BUD.biz_owner, BUD.contact_window, BUD.customer, BUD.site,
BUD.plan_start, BUD.plan_finish, BUD.recv_ep_code, BUD.comments, BUD.cancelled, BUD.bud_syst_recv_chg_dept, BUD.bu, BUD.handle_div, BUD.project_category, BUD.project_type, BUD.recv_chg_dept, '' AS bud_plan, DIV.div_group FROM imp_bud BUD, imp_div DIV WHERE BUD.handle_div = DIV.div """
        BU_ID_QUERY = "AND BUD.id = %s "
        COMMON_ORDER = "ORDER BY BUD.project_year, BUD.project_name"
        with connection.cursor() as cursor:
            if bud_id:
                COMMON_QUERY = COMMON_QUERY + BU_ID_QUERY
                sqlParameters.append(bud_id)
            cursor.execute(COMMON_QUERY + COMMON_ORDER, sqlParameters)

            result = namedtuplefetchall(cursor)
            return Response(result)

    @swagger_auto_schema(
        method='post',
        operation_summary="Query budget project",
        operation_description="Query budget project",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "project_year": openapi.Schema(type=openapi.TYPE_STRING, description="Budget Project Year"),
                "project_name": openapi.Schema(type=openapi.TYPE_STRING, description="Budget Project"),
                "it_pm": openapi.Schema(type=openapi.TYPE_STRING, description="IT PM"),
                "site": openapi.Schema(type=openapi.TYPE_STRING, description="site"),
                "plan_start": openapi.Schema(type=openapi.TYPE_STRING, description="plan start"),
                "plan_finish": openapi.Schema(type=openapi.TYPE_STRING, description="plan finish"),
                "project_category": openapi.Schema(type=openapi.TYPE_STRING, description="project category"),
                "project_type": openapi.Schema(type=openapi.TYPE_STRING, description="project type"),
                "bu": openapi.Schema(type=openapi.TYPE_STRING, description="bu"),
                "handle_div": openapi.Schema(type=openapi.TYPE_STRING, description="handle division"),
                "cancel": openapi.Schema(type=openapi.TYPE_STRING, description="cancel"),
            }
        ),
    )
    @action(detail=False, methods=["post"])
    def query_bud(self, request, pk=None):
        sqlParameters = []
        req = request.data
        project_year = req.get("project_year")
        project_name = req.get("project_name")
        it_pm = req.get("it_pm")
        site = req.get("site")
        plan_date_star = req.get("plan_start")
        plan_date_end = req.get("plan_finish")
        project_cate = req.get("project_category")
        project_type = req.get("project_type")
        bu = req.get("bu")
        handle_div = req.get("handle_div")
        cancel = req.get("cancelled")

        COMMON_QUERY = """SELECT BUD.id, BUD.project_year, BUD.project_name, BUD.it_pm, BUD.biz_owner, BUD.contact_window, BUD.customer, BUD.site,
BUD.plan_start, BUD.plan_finish, BUD.recv_ep_code, BUD.comments, BUD.cancelled, BUD.bud_syst_recv_chg_dept, BUD.bu, BUD.handle_div, BUD.project_category, BUD.project_type, BUD.recv_chg_dept, '' AS bud_plan, DIV.div_group FROM imp_bud BUD, imp_div DIV WHERE BUD.handle_div = DIV.div """
        PY_QUERY = "AND UPPER(BUD.project_year) = UPPER(%s) "
        PN_QUERY = "AND UPPER(BUD.project_name) LIKE UPPER(%s) "
        IP_QUERY = "AND UPPER(BUD.it_pm) LIKE UPPER (%s) "
        SITE_QUERY = "AND UPPER(BUD.site) LIKE UPPER (%s) "
        PS_QUERY = "AND BUD.plan_start >= %s "
        PE_QUERY = "AND BUD.plan_finish <= %s "
        PC_QUERY = "AND BUD.project_category = %s "
        PT_QUERY = "AND BUD.project_type = %s "
        BU_QUERY = "AND BUD.bu = %s "
        HD_QUERY = "AND BUD.handle_div = %s "
        CL_QUERY = "AND BUD.cancelled = %s "
        COMMON_ORDER = "ORDER BY BUD.project_year, BUD.project_name, BUD.cancelled ASC"

        with connection.cursor() as cursor:
            if project_year:
                COMMON_QUERY = COMMON_QUERY + PY_QUERY
                sqlParameters.append(project_year)
            if project_name:
                COMMON_QUERY = COMMON_QUERY + PN_QUERY
                sqlParameters.append(project_name + "%")
            if it_pm:
                COMMON_QUERY = COMMON_QUERY + IP_QUERY
                sqlParameters.append("%" + it_pm + "%")
            if site:
                COMMON_QUERY = COMMON_QUERY + SITE_QUERY
                sqlParameters.append("%" + site + "%")
            if plan_date_star:
                COMMON_QUERY = COMMON_QUERY + PS_QUERY
                sqlParameters.append(plan_date_star)
            if plan_date_end:
                COMMON_QUERY = COMMON_QUERY + PE_QUERY
                sqlParameters.append(plan_date_end)
            if project_cate:
                COMMON_QUERY = COMMON_QUERY + PC_QUERY
                sqlParameters.append(project_cate)
            if project_type:
                COMMON_QUERY = COMMON_QUERY + PT_QUERY
                sqlParameters.append(project_type)
            if bu:
                COMMON_QUERY = COMMON_QUERY + BU_QUERY
                sqlParameters.append(bu)
            if handle_div:
                COMMON_QUERY = COMMON_QUERY + HD_QUERY
                sqlParameters.append(handle_div)
            if cancel:
                COMMON_QUERY = COMMON_QUERY + CL_QUERY
                sqlParameters.append(cancel)

            cursor.execute(COMMON_QUERY + COMMON_ORDER, sqlParameters)

            result = namedtuplefetchall(cursor)
            return Response(result)

    @action(detail=False, methods=["post"])
    def query_bud_by_upload(self, request, pk=None):
        sqlParameters = []
        req = request.data
        project_year = req.get("project_year").upper().split(",")
        project_name = req.get("project_name").upper().split(",")
        # [2*a for a in x if a % 2 == 1]
        COMMON_QUERY = """SELECT BUD.id, BUD.project_year, BUD.project_name, BUD.it_pm, BUD.biz_owner, BUD.contact_window, BUD.customer, BUD.site, BUD.plan_start, BUD.plan_finish, BUD.recv_ep_code, BUD.comments, BUD.cancelled, BUD.bud_syst_recv_chg_dept, BUD.bu, BUD.handle_div, BUD.project_category, BUD.project_type, BUD.recv_chg_dept, '' AS bud_plan, DIV.div_group FROM imp_bud BUD, imp_div DIV WHERE BUD.handle_div = DIV.div """
        PY_QUERY = "AND BUD.project_year = ANY(%s) "
        PN_QUERY = "AND UPPER(BUD.project_name) = ANY(%s) "
        COMMON_ORDER = "ORDER BY BUD.project_year, BUD.project_name, BUD.cancelled ASC"

        with connection.cursor() as cursor:
            if project_year:
                COMMON_QUERY = COMMON_QUERY + PY_QUERY
                sqlParameters.append(project_year)

            if project_name:
                COMMON_QUERY = COMMON_QUERY + PN_QUERY
                sqlParameters.append(project_name)

            cursor.execute(COMMON_QUERY + COMMON_ORDER, sqlParameters)

            result = namedtuplefetchall(cursor)
            return Response(result)


def namedtuplefetchall(cursor):
    # Return all rows from a cursor as a namedtuple
    # desc = cursor.description
    nt_result = namedtuple(
        "Result",
        [
            "id",
            "project_year",
            "project_name",
            "it_pm",
            "biz_owner",
            "contact_window",
            "customer",
            "site",
            "plan_start",
            "plan_finish",
            "recv_ep_code",
            "comments",
            "cancelled",
            "bud_syst_recv_chg_dept",
            "bu",
            "handle_div",
            "project_category",
            "project_type",
            "recv_chg_dept",
            "bud_plan",
            "div_group",
        ],
    )
    result = [nt_result(*row) for row in cursor.fetchall()]
    result = [
        {
            "id": r.id,
            "project_year": r.project_year,
            "project_name": r.project_name,
            "it_pm": r.it_pm,
            "biz_owner": r.biz_owner,
            "contact_window": r.contact_window,
            "customer": r.customer,
            "site": r.site,
            "plan_start": r.plan_start,
            "plan_finish": r.plan_finish,
            "recv_ep_code": r.recv_ep_code,
            "comments": r.comments,
            "cancelled": r.cancelled,
            "bud_syst_recv_chg_dept": r.bud_syst_recv_chg_dept,
            "bu": r.bu,
            "div": r.handle_div,
            "div_group": r.div_group,
            "project_category": r.project_category,
            "project_type": r.project_type,
            "recv_chg_dept": r.recv_chg_dept,
            "bud_plan": getBudplan(r.id, r.project_year, r.project_name),
        }
        for r in result
    ]
    return result


def getBudplan(bud_id, project_year, project_name):
    COMMON_QUERY = """SELECT BUDLN.id, BUDLN.bud_id, BUDLN.jan_plan, BUDLN.feb_plan, BUDLN.mar_plan, BUDLN.apr_plan, BUDLN.may_plan, BUDLN.jun_plan, BUDLN.jul_plan, BUDLN.aug_plan, BUDLN.sep_plan, BUDLN.oct_plan, BUDLN.nov_plan, BUDLN.dec_plan, BUDLN.resource, RES.div_group, RES.div_code FROM imp_budln BUDLN LEFT JOIN (SELECT A.resource_group, A.div_group_id, A.division as div_group, B.div AS div_code FROM imp_resource A, imp_div B WHERE A.div_group_id = B.id) RES ON UPPER(BUDLN.resource) = UPPER(RES.resource_group) WHERE BUDLN.bud_id = %s AND BUDLN.project_year = %s AND BUDLN.project_name = %s"""
    COMMON_ORDER = "ORDER BY BUDLN.bud_id, RES.resource_group ASC"
    with connection.cursor() as cursor:
        cursor.execute(
            COMMON_QUERY + COMMON_ORDER, [bud_id, project_year, project_name]
        )
        result = namedtuplefetchallPlan(cursor)
        return result


def namedtuplefetchallPlan(cursor):
    # Return all rows from a cursor as a namedtuple
    # desc = cursor.description
    nt_result = namedtuple(
        "Result",
        [
            "id",
            "bud_id",
            "jan_plan",
            "feb_plan",
            "mar_plan",
            "apr_plan",
            "may_plan",
            "jun_plan",
            "jul_plan",
            "aug_plan",
            "sep_plan",
            "oct_plan",
            "nov_plan",
            "dec_plan",
            "resource",
            "div_group",
            "div_code"
        ],
    )
    result = [nt_result(*row) for row in cursor.fetchall()]
    result = [
        {
            "id": r.id,
            "bud_id": r.bud_id,
            "jan_plan": r.jan_plan,
            "feb_plan": r.feb_plan,
            "mar_plan": r.mar_plan,
            "apr_plan": r.apr_plan,
            "may_plan": r.may_plan,
            "jun_plan": r.jun_plan,
            "jul_plan": r.jul_plan,
            "aug_plan": r.aug_plan,
            "sep_plan": r.sep_plan,
            "oct_plan": r.oct_plan,
            "nov_plan": r.nov_plan,
            "dec_plan": r.dec_plan,
            "resource": r.resource,
            "div_group": r.div_group,
            "div_code": r.div_code
        }
        for r in result
    ]
    return result
