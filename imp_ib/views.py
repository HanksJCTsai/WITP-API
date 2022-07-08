import calendar
from datetime import datetime
from django.db import connection
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework import permissions, viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from collections import namedtuple

from .models import ImpIb
from .serializers import ImpIbSerializer

# Create your views here.

class ImpIbViewSet(viewsets.ModelViewSet):
    serializer_class = ImpIbSerializer
    queryset = ImpIb.objects.filter()

    def get_permissions(self):
        # 決定哪些method需要哪些認證
        # GET不用
        if self.request.method in ["POST","PUT","PATCH","DELETE"]:
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.AllowAny()]

    @swagger_auto_schema(
        method='post',
        operation_summary='Actual Confirm report data',
        operation_description="Get Actual Confirm report data",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "project_year": openapi.Schema(type=openapi.TYPE_STRING, description="IB Project Year"),
                "project_name": openapi.Schema(type=openapi.TYPE_STRING, description="IB Project"),
                "ib_code": openapi.Schema(type=openapi.TYPE_STRING, description="IB Code"),
                "it_pm": openapi.Schema(type=openapi.TYPE_STRING, description="IT PM"),
                "cancelled": openapi.Schema(type=openapi.TYPE_STRING, description="Cancelle"),
                "complete": openapi.Schema(type=openapi.TYPE_STRING, description="Complete"),
                "paj_monthly_done": openapi.Schema(type=openapi.TYPE_STRING, description="PAJ monthly done"),
            },
            required=["project_year","project_name","ib_code","cancelled","complete","paj_monthly_done"]
        ),
    )
    @action(detail=False, methods=["post"])
    def getActualConfirmReportData(self, request, pk=None):
        sqlParameters = []
        req = request.data
        project_year = req.get("project_year")
        project_name = req.get("project_name")
        ib_code = req.get("ib_code")
        it_pm = req.get("it_pm")
        cancel = req.get("cancelled")
        complete = req.get("complete")
        monthly_paj_done = req.get("monthly_paj_done")
        plan_start = datetime.strptime(project_year, "%Y").strftime("%Y-01-01")
        plan_finish = (datetime(datetime.strptime(project_year, "%Y").year, ((datetime.now()).month -1 ), calendar.monthrange((datetime.now()).year, ((datetime.now()).month -1))[1])).strftime("%Y-%m-%d")
        last_month_initialism = (datetime(datetime.strptime(project_year, "%Y").year, ((datetime.now()).month -1 ), calendar.monthrange((datetime.now()).year, ((datetime.now()).month -1))[1])).strftime("%b").lower()

        COMMON_QUERY = """SELECT IB.project_year, IB.project_name, IB.ib_code, IB.ep_code, IB.it_pm, IB.plan_start, IB.plan_finish, IB.handle_div,
 IB.cancelled, IB.complete, IB.monthly_paj_done, '' AS pajln FROM imp_ib IB WHERE 1=1 """
        PY_QUERY = "AND IB.project_year = %s "
        PN_QUERY = "AND UPPER(IB.project_name) LIKE UPPER(%s) "
        IB_QUERY = "AND UPPER(IB.ib_code) LIKE UPPER (%s) "
        IT_QUERY = "AND UPPER(IB.it_pm) LIKE UPPER (%s) "
        PF_QUERY = "AND (IB.plan_start >= %s AND IB.plan_start <= %s)"
        CL_QUERY = "AND IB.cancelled = %s "
        CP_QUERY = "AND IB.complete = %s "
        MP_QUERY = "AND IB.monthly_paj_done = %s "
        COMMON_ORDER = "ORDER BY IB.project_year, IB.project_name, IB.cancelled, IB.complete, IB.monthly_paj_done ASC"

        with connection.cursor() as cursor:
            if project_year:
                COMMON_QUERY = COMMON_QUERY + PY_QUERY
                sqlParameters.append(project_year)
            if project_name:
                COMMON_QUERY = COMMON_QUERY + PN_QUERY
                sqlParameters.append("%" + project_name + "%")
            if ib_code:
                COMMON_QUERY = COMMON_QUERY + IB_QUERY
                sqlParameters.append("%" + ib_code + "%")
            if it_pm:
                COMMON_QUERY = COMMON_QUERY + IT_QUERY
                sqlParameters.append("%" + it_pm + "%")
            if plan_finish:
                COMMON_QUERY = COMMON_QUERY + PF_QUERY
                sqlParameters.append(plan_start)
                sqlParameters.append(plan_finish)
            if cancel:
                COMMON_QUERY = COMMON_QUERY + CL_QUERY
                sqlParameters.append(cancel)
            if complete:
                COMMON_QUERY = COMMON_QUERY + CP_QUERY
                sqlParameters.append(complete)
            if monthly_paj_done:
                COMMON_QUERY = COMMON_QUERY + MP_QUERY
                sqlParameters.append(monthly_paj_done)

            cursor.execute(COMMON_QUERY + COMMON_ORDER, sqlParameters)
            results = namedtuplefetchall_ActualComfirm(cursor)

            responses = []

            for ibItem in results:
                monthly_done = True
                for pajlnItem in ibItem.get("pajln"):
                    check_monthly = last_month_initialism + "_plan"
                    if check_monthly in pajlnItem:
                       monthly_done = float(pajlnItem.get(check_monthly)) >0
                       if monthly_done == False:
                           response = {
                               "project_year": ibItem.get("project_year"),
                                "project_name": ibItem.get("project_name"),
                                "ib_code": ibItem.get("ib_code"),
                                "ep_code":ibItem.get("ep_code"),
                                "it_pm":ibItem.get("it_pm"),
                                "plan_start":ibItem.get("plan_start"),
                                "plan_finish":ibItem.get("plan_finish"),
                                "handle_div":ibItem.get("handle_div"),
                                "cancelled":ibItem.get("cancelled"),
                                "complete":ibItem.get("complete"),
                                "monthly_paj_done": "Y" if monthly_done else "N",
                           }
                           responses.append(response)
                           break
                    else:
                        monthly_done = False
                        response = {
                            "project_year": ibItem.get("project_year"),
                            "project_name": ibItem.get("project_name"),
                            "ib_code": ibItem.get("ib_code"),
                            "ep_code":ibItem.get("ep_code"),
                            "it_pm":ibItem.get("it_pm"),
                            "plan_start":ibItem.get("plan_start"),
                            "plan_finish":ibItem.get("plan_finish"),
                            "handle_div":ibItem.get("handle_div"),
                            "cancelled":ibItem.get("cancelled"),
                            "complete":ibItem.get("complete"),
                            "monthly_paj_done": "Y" if monthly_done else "N",
                        }
                        responses.append(response)
                        break
        return Response(responses)

    @action(detail=False, methods=["post"])
    def query_ib(self, request, pk=None):
        sqlParameters = []
        req = request.data
        project_year = req.get("project_year")
        project_name = req.get("project_name")
        it_pm = req.get("it_pm")
        monthly_paj_done = req.get("monthly_paj_done")
        handle_div = req.get("handle_div")
        cancel = req.get("cancelled")
        complete = req.get("complete")
        ib_code = req.get("ib_code")
        ep_code = req.get("ep_code")

        COMMON_QUERY = """SELECT IB.id, IB.project_year, IB.project_name, IB.it_pm, IB.plan_start, IB.plan_finish, IB.ib_code, IB.ep_code,
IB.pmcs_ib_project_name, IB.pmcs_ep_project_name, IB.cancelled, IB.complete, IB.monthly_paj_done, IB.handle_div,
IB.creatdate, IB.creater, IB.updatedate, IB.updater, '' as ib_ln FROM imp_ib IB WHERE 1=1 """
        PY_QUERY = "AND IB.project_year = %s "
        PN_QUERY = "AND UPPER(IB.project_name) LIKE UPPER(%s) "
        IP_QUERY = "AND UPPER(IB.it_pm) LIKE UPPER (%s) "
        IB_QUERY = "AND UPPER(IB.ib_code) LIKE UPPER (%s) "
        EP_QUERY = "AND UPPER(IB.ep_code) LIKE UPPER (%s) "
        HD_QUERY = "AND IB.handle_div = %s "
        CL_QUERY = "AND IB.cancelled = %s "
        CP_QUERY = "AND IB.complete = %s "
        MP_QUERY = "AND IB.monthly_paj_done = %s "
        COMMON_ORDER = "ORDER BY IB.project_year, IB.project_name, IB.cancelled, IB.complete, IB.monthly_paj_done ASC"

        with connection.cursor() as cursor:
            if project_year:
                COMMON_QUERY = COMMON_QUERY + PY_QUERY
                sqlParameters.append(project_year)
            if project_name:
                COMMON_QUERY = COMMON_QUERY + PN_QUERY
                sqlParameters.append("%" + project_name + "%")
            if it_pm:
                COMMON_QUERY = COMMON_QUERY + IP_QUERY
                sqlParameters.append("%" + it_pm + "%")
            if handle_div:
                COMMON_QUERY = COMMON_QUERY + HD_QUERY
                sqlParameters.append(handle_div)
            if cancel:
                COMMON_QUERY = COMMON_QUERY + CL_QUERY
                sqlParameters.append(cancel)
            if complete:
                COMMON_QUERY = COMMON_QUERY + CP_QUERY
                sqlParameters.append(complete)
            if ib_code:
                COMMON_QUERY = COMMON_QUERY + IB_QUERY
                sqlParameters.append("%" + ib_code + "%")
            if ep_code:
                COMMON_QUERY = COMMON_QUERY + EP_QUERY
                sqlParameters.append("%" + ep_code + "%")
            if monthly_paj_done:
                COMMON_QUERY = COMMON_QUERY + MP_QUERY
                sqlParameters.append(monthly_paj_done)

            cursor.execute(COMMON_QUERY + COMMON_ORDER, sqlParameters)

            result = namedtuplefetchall(cursor)
            return Response(result)

    @action(detail=False, methods=["post"])
    def query_ib_by_upload(self, request, pk=None):
        sqlParameters = []
        req = request.data
        project_year = req.get("project_year").upper().split(",")
        project_name = req.get("project_name").upper().split(",")

        COMMON_QUERY = """SELECT IB.id, IB.project_year, IB.project_name, IB.it_pm, IB.plan_start, IB.plan_finish, IB.ib_code, IB.ep_code,
IB.pmcs_ib_project_name, IB.pmcs_ep_project_name, IB.cancelled, IB.complete, IB.handle_div, IB.monthly_paj_done,
IB.creatdate, IB.creater, IB.updatedate, IB.updater FROM imp_ib IB WHERE 1=1 """
        PY_QUERY = "AND IB.project_year = ANY(%s) "
        PN_QUERY = "AND UPPER(IB.project_name) = ANY(%s) "
        COMMON_ORDER = "ORDER BY IB.project_year, IB.project_name, IB.cancelled, IB.complete, IB.monthly_paj_done ASC"

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

def getIBln(ib_id, project_year, project_name):
    COMMON_QUERY = """SELECT IBLN.id, IBLN.ib_id, IBLN.jan_plan, IBLN.feb_plan, IBLN.mar_plan, IBLN.apr_plan, IBLN.may_plan,
IBLN.jun_plan, IBLN.jul_plan, IBLN.aug_plan, IBLN.sep_plan, IBLN.oct_plan, IBLN.nov_plan, IBLN.dec_plan,
IBLN.div_group, IBLN.creatdate, IBLN.creater, IBLN.updatedate, IBLN.updater FROM imp_ibln IBLN WHERE IBLN.ib_id = %s AND IBLN.project_year = %s AND IBLN.project_name = %s """
    COMMON_ORDER = "ORDER BY IBLN.ib_id, IBLN.div_group ASC"
    with connection.cursor() as cursor:
        cursor.execute(
            COMMON_QUERY + COMMON_ORDER, [ib_id, project_year, project_name]
        )
        result = namedtuplefetchallPlan(cursor)
        return result

def getPajln(project_year, project_name, ib_code):
    COMMON_QUERY = """SELECT PAJLN.project_year, PAJLN.project_name, PAJLN.ib_code, PAJLN.jan_plan, PAJLN.feb_plan, PAJLN.mar_plan, PAJLN.apr_plan, PAJLN.may_plan, PAJLN.jun_plan, PAJLN.jul_plan, PAJLN.aug_plan, PAJLN.sep_plan, PAJLN.oct_plan, PAJLN.nov_plan, PAJLN.dec_plan, PAJLN.div_group FROM imp_pajln PAJLN WHERE PAJLN.project_year = %s AND PAJLN.project_name = %s AND PAJLN.ib_code = %s"""
    COMMON_ORDER = "ORDER BY PAJLN.project_year, PAJLN.project_name, PAJLN.ib_code, PAJLN.div_group ASC"
    with connection.cursor() as cursor:
        cursor.execute(
            COMMON_QUERY + COMMON_ORDER, [project_year, project_name, ib_code]
        )
        result = namedtuplefetchallPajln(cursor)
        return result

def namedtuplefetchall_ActualComfirm(cursor):
    # Return all rows from a cursor as a namedtuple
    # desc = cursor.description
    nt_result = namedtuple(
        "Result",
        [
            "project_year",
            "project_name",
            "ib_code",
            "ep_code",
            "it_pm",
            "plan_start",
            "plan_finish",
            "handle_div",
            "cancelled",
            "complete",
            "monthly_paj_done",
            "pajln"
        ],
    )
    result = [nt_result(*row) for row in cursor.fetchall()]
    result = [
        {
            "project_year": r.project_year,
            "project_name": r.project_name,
            "ib_code": r.ib_code,
            "ep_code": r.ep_code,
            "it_pm": r.it_pm,
            "plan_start": r.plan_start,
            "plan_finish": r.plan_finish,
            "handle_div": r.handle_div,
            "cancelled": r.cancelled,
            "complete": r.complete,
            "monthly_paj_done": r.monthly_paj_done,
            "pajln": getPajln(r.project_year, r.project_name, r.ib_code)
        }
        for r in result
    ]
    return result

def namedtuplefetchallPajln(cursor):
    # Return all rows from a cursor as a namedtuple
    # desc = cursor.description
    nt_result = namedtuple(
        "Result",
        [
            "project_year",
            "project_name",
            "ib_code",
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
            "div_group"
        ],
    )
    result = [nt_result(*row) for row in cursor.fetchall()]
    result = [
        {
            "project_year":r.project_year,
            "project_name":r.project_name,
            "ib_code":r.ib_code,
            "jan_plan":r.jan_plan,
            "feb_plan":r.feb_plan,
            "mar_plan":r.mar_plan,
            "apr_plan":r.apr_plan,
            "may_plan":r.may_plan,
            "jun_plan":r.jun_plan,
            "jul_plan":r.jul_plan,
            "aug_plan":r.aug_plan,
            "sep_plan":r.sep_plan,
            "oct_plan":r.oct_plan,
            "nov_plan":r.nov_plan,
            "dec_plan":r.dec_plan,
            "div_group":r.div_group
        }
        for r in result
    ]
    return result

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
            "plan_start",
            "plan_finish",
            "ib_code",
            "pmcs_ib_project_name",
            "ep_code",
            "pmcs_ep_project_name",
            "cancelled",
            "complete",
            "monthly_paj_done",
            "handle_div",
            "creatdate",
            "creater",
            "updatedate",
            "updater",
            "ib_ln",
        ],
    )
    result = [nt_result(*row) for row in cursor.fetchall()]
    result = [
        {
            "id": r.id,
            "project_year": r.project_year,
            "project_name": r.project_name,
            "it_pm": r.it_pm,
            "plan_start": r.plan_start,
            "plan_finish": r.plan_finish,
            "ib_code": r.ib_code,
            "pmcs_ib_project_name": r.pmcs_ib_project_name,
            "ep_code": r.ep_code,
            "pmcs_ep_project_name": r.pmcs_ep_project_name,
            "cancelled": r.cancelled,
            "complete": r.complete,
            "monthly_paj_done": r.monthly_paj_done,
            "handle_div": r.handle_div,
            "creatdate": r.creatdate,
            "creater": r.creater,
            "updatedate": r.updatedate,
            "updater": r.updater,
            "ib_ln": getIBln(r.id, r.project_year, r.project_name),
        }
        for r in result
    ]
    return result

def namedtuplefetchallPlan(cursor):
    # Return all rows from a cursor as a namedtuple
    # desc = cursor.description
    nt_result = namedtuple(
        "Result",
        [
            "id",
            "ib_id",
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
            "div_group",
            "creatdate",
            "creater",
            "updatedate",
            "updater",
        ],
    )
    result = [nt_result(*row) for row in cursor.fetchall()]
    result = [
        {
            "id": r.id,
            "ib_id": r.ib_id,
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
            "div_group": r.div_group,
            "creatdate": r.creatdate,
            "creater": r.creater,
            "updatedate": r.updatedate,
            "updater": r.updater
        }
        for r in result
    ]
    return result
