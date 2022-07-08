import calendar
from datetime import datetime
from multiprocessing.spawn import import_main_path
from unittest import result
from urllib import response
from django.db import connection
from django.http import JsonResponse
from rest_framework.decorators import action
from rest_framework import permissions, viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from collections import namedtuple
from django.db.models.query_utils import Q

from .models import PajMonth
from .serializers import PajMonthSerializer

# Create your views here.


class PajMonthViewSet(viewsets.ModelViewSet):
    serializer_class = PajMonthSerializer
    queryset = PajMonth.objects.filter()

    def get_permissions(self):
        # 決定哪些method需要哪些認證
        # GET不用
        if self.request.method in ["POST","PUT","PATCH","DELETE"]:
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.AllowAny()]

    @action(detail=False, methods=["POST"])
    def query_pajmonth(self, request):
        response =  {"code": 0,"msg": " ","data": []}
        sqlParameters = []
        req = request.data
        project_year = req.get("project_year")
        project_name = req.get("project_name")
        plan_finish = (datetime((datetime.now()).year, ((datetime.now()).month -1 ), calendar.monthrange((datetime.now()).year, ((datetime.now()).month -1))[1])).strftime("%Y-%m-%d")
        ib_code = req.get("ib_code")
        ep_code = req.get("ep_code")
        last_month = str((datetime.now()).month -1).zfill(2)
        try:
            COMMON_QUERY = """SELECT IB.id, IB.project_year, IB.project_name, IB.it_pm, IB.plan_start, IB.plan_finish, IB.ib_code, IB.ep_code,
    IB.pmcs_ib_project_name, IB.pmcs_ep_project_name, IB.cancelled, IB.complete, IB.monthly_paj_done, IB.handle_div,
    IB.creatdate, IB.creater, IB.updatedate, IB.updater, (SELECT COUNT(PAJMON.ref) AS ref FROM  imp_pajmonth PAJMON WHERE PAJMON.project_year = %s AND PAJMON.project_month = %s) AS paj_monthly_flag FROM imp_ib IB WHERE 1=1 """
            PY_QUERY = "AND IB.project_year = %s "
            PN_QUERY = "AND UPPER(IB.project_name) LIKE UPPER(%s) "
            PF_QUERY = "AND (IB.plan_start >= %s AND IB.plan_start <= %s) "
            IB_QUERY = "AND UPPER(IB.ib_code) LIKE UPPER (%s) "
            EP_QUERY = "AND UPPER(IB.ep_code) LIKE UPPER (%s) "
            COMMON_ORDER = "ORDER BY IB.project_year, IB.project_name, IB.cancelled, IB.complete, IB.monthly_paj_done ASC"
            sqlParameters.append(project_year)
            sqlParameters.append(last_month)
            with connection.cursor() as cursor:
                if project_year:
                    COMMON_QUERY = COMMON_QUERY + PY_QUERY
                    sqlParameters.append(project_year)
                if project_name:
                    COMMON_QUERY = COMMON_QUERY + PN_QUERY
                    sqlParameters.append("%" + project_name + "%")
                if plan_finish:
                    COMMON_QUERY = COMMON_QUERY + PF_QUERY
                    sqlParameters.append(datetime.now().strftime("%Y-01-01"))
                    sqlParameters.append(plan_finish)
                if ib_code:
                    COMMON_QUERY = COMMON_QUERY + IB_QUERY
                    sqlParameters.append("%" + ib_code + "%")
                if ep_code:
                    COMMON_QUERY = COMMON_QUERY + EP_QUERY
                    sqlParameters.append("%" + ep_code + "%")
                cursor.execute(COMMON_QUERY + COMMON_ORDER, sqlParameters)
                result = namedtuplefetchall(cursor)
                msg = ""
                if len(result) > 0:
                    if int(result[0]["paj_monthly_flag"]) == 0:
                        msg =  ((datetime.now()).month -1 ).strftime("%M") + " has completed monthly end!"
                    response["code"] = 1
                    response["msg"] = msg
                    response["data"] = result
                else :
                    response["code"] = 1
                    response["msg"] = "No Data!"
                    response["data"] = result
                return JsonResponse(response)
        except Exception as e:
            response["code"] = 2
            response["msg"] = e
            return JsonResponse(response)

    @action(detail = False, methods=(["POST"]))
    def update_pajmonthly_end(self, request):
        response =  {"code": 0,"msg": ""}
        req = request.data
        project_year = req.get("project_year")
        project_month = req.get("project_month")
        ref = req.get("ref")
        try:
            ImpPajmonth = PajMonth.objects.filter(Q(project_year = project_year) & Q(project_month = project_month))
            tmp_pajmonth = {}
            tmp_pajmonth["ref"] = ref
            tmp_pajmonth["project_year"] = str(project_year)
            tmp_pajmonth["project_month"] = str(project_month)
            if len(ImpPajmonth) :
                paj_monthly = PajMonth.objects.filter(id = ImpPajmonth.get().id).update(**tmp_pajmonth)
                if paj_monthly > 0 :
                    response["code"] =1
                    response["msg"] = "Update success!"
            else :
                paj_monthly = PajMonth.objects.create(**tmp_pajmonth)
                if paj_monthly.id > 0 :
                    response["code"] =1
                    response["msg"] = "Create success!"
            return JsonResponse(response)
        except Exception as e:
            response["code"] = 2
            response["msg"] = e
            return JsonResponse(response)


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
            "paj_monthly_flag"
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
            "paj_monthly_flag": r.paj_monthly_flag
        }
        for r in result
    ]
    return result
