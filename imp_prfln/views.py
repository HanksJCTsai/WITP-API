import json
from django.db import connection
from django.http import JsonResponse
from rest_framework import permissions, viewsets
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from collections import namedtuple
from django.core import serializers

from .models import ImpPrfln
from .serializers import ImpPrflnSerializer
from django.db.models import Q
# Create your views here.


class ImpPrflnViewSet(viewsets.ModelViewSet):
    serializer_class = ImpPrflnSerializer
    queryset = ImpPrfln.objects.filter()

    def get_permissions(self):
        # 決定哪些method需要哪些認證
        # GET不用
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.AllowAny()]

    @swagger_auto_schema(
        method='post',
        operation_summary='Get prf detail data by project year, name, ib id',
        operation_description="Get prf detail data by project year, name, ib id",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "project_year": openapi.Schema(type=openapi.TYPE_STRING, description="PRF Project Year"),
                "project_name": openapi.Schema(type=openapi.TYPE_STRING, description="PRF Project"),
                "prf_id": openapi.Schema(type=openapi.TYPE_STRING, description="PRF id"),
            },
            required=["project_year","project_name","prf_id"]
        ),
    )
    @action(detail=False, methods=["post"])
    def query_prflns(self, request, pk=None):
        try:
            data = {"code": 0, "msg": "", "data": " "}
            req = request.data
            project_year = req.get("project_year")
            project_name = req.get("project_name")
            prf_id = req.get("prf_id")
            result = ImpPrfln.objects.filter(Q(prf_id=prf_id) & Q(project_name=project_name) & Q(project_year=project_year))
            data["code"] = 1
            data["msg"] = "Get PRF Detail data by prf id or project year or project name"
            data["data"] = json.loads(serializers.serialize("json", result))
            return JsonResponse(data)
        except Exception as e:
            data["code"] = 2
            data["msg"] = "Error message:" + str(e)
            data["data"] = json.loads(serializers.serialize("json", {}))
            return JsonResponse(data)

    @action(detail=False, methods=["post"])
    def query_budln(self, request, pk=None):
        sqlParameters = []
        req = request.data
        project_year = req.get("project_year")
        project_name = req.get("project_name")
        div_group = req.get("div_group")
        COMMON_QUERY = """SELECT PRFLN.id, PRFLN.prf_id, PRFLN.jan_plan, PRFLN.feb_plan, PRFLN.mar_plan, PRFLN.apr_plan, PRFLN.may_plan,
PRFLN.jun_plan, PRFLN.jul_plan, PRFLN.aug_plan, PRFLN.sep_plan, PRFLN.oct_plan, PRFLN.nov_plan, PRFLN.dec_plan,
PRFLN.div_group, PRFLN.creatdate, PRFLN.creater, PRFLN.updatedate, PRFLN.updater, div."div", div."functions FROM imp_prfln PRFLN LEFT JOIN imp_div div ON PRFLN.div_group = div.div_group WHERE 1=1 """
        YEAR_QUERY = "AND UPPER(PRFLN.project_year) = UPPER(%s) "
        NAME_QUERY = "AND UPPER(PRFLN.project_name) LIKE UPPER(%s) "
        DIV_GROUP_QUERY = "AND PRFLN.div_group = %s "
        COMMON_ORDER = (
            "ORDER BY PRFLN.project_year, PRFLN.project_name, PRFLN.div_group ASC"
        )

        with connection.cursor() as cursor:
            if project_year:
                COMMON_QUERY = COMMON_QUERY + YEAR_QUERY
                sqlParameters.append(project_year.upper())
            if project_name:
                COMMON_QUERY = COMMON_QUERY + NAME_QUERY
                sqlParameters.append(project_name.upper() + "%")
            if div_group:
                COMMON_QUERY = COMMON_QUERY + DIV_GROUP_QUERY
                sqlParameters.append(div_group)

            cursor.execute(COMMON_QUERY + COMMON_ORDER, sqlParameters)

            result = namedtuplefetchallPlan(cursor)
            return Response(result)


def namedtuplefetchallPlan(cursor):
    # Return all rows from a cursor as a namedtuple
    # desc = cursor.description
    nt_result = namedtuple(
        "Result",
        [
            "id",
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
            "div",
            "functions",
        ],
    )
    result = [nt_result(*row) for row in cursor.fetchall()]
    result = [
        {
            "id": r.id,
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
            "creatdate":r.creatdate,
            "creater":r.creater,
            "updatedate":r.updatedate,
            "updater":r.updater,
            "div":r.div,
            "functions":r.functions
        }
        for r in result
    ]
    return result
