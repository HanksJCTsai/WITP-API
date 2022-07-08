from django.db import connection
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from collections import namedtuple

from .models import ImpBudln
from .serializers import ImpBudlnSerializer

# Create your views here.


class ImpBudlnViewSet(viewsets.ModelViewSet):
    serializer_class = ImpBudlnSerializer
    queryset = ImpBudln.objects.filter()

    def get_permissions(self):
        # 決定哪些method需要哪些認證
        # GET不用
        if self.request.method in ["POST","PUT","PATCH","DELETE"]:
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.AllowAny()]

    @action(detail=False, methods=["post"])
    def query_budln(self, request, pk=None):
        sqlParameters = []
        req = request.data
        project_year = req.get("project_year")
        project_name = req.get("project_name")
        resource = req.get("resource")
        COMMON_QUERY = """ SELECT BUDLN.id, BUDLN.project_year, BUDLN.project_name, BUDLN.bud_id, BUDLN.jan_plan, BUDLN.feb_plan, BUDLN.mar_plan, BUDLN.apr_plan, BUDLN.may_plan, BUDLN.jun_plan, BUDLN.jul_plan, BUDLN.aug_plan, BUDLN.sep_plan, BUDLN.oct_plan, BUDLN.nov_plan, BUDLN.dec_plan, BUDLN.resource , RES.resource_group, RES.div_group FROM imp_budln BUDLN LEFT JOIN (SELECT A.resource_group, A.div_group_id, A.division as div_group, B.div AS div_code FROM imp_resource A, imp_div B WHERE A.div_group_id = B.id) RES ON UPPER(BUDLN.resource) = UPPER(RES.resource_group) WHERE 1=1 """
        YEAR_QUERY = "AND UPPER(BUDLN.project_year) = UPPER(%s) "
        NAME_QUERY = "AND UPPER(BUDLN.project_name) LIKE UPPER(%s) "
        RESOURCE_QUERY = "AND BUDLN.resource = %s "
        COMMON_ORDER = ("ORDER BY BUDLN.project_year, BUDLN.project_name, RES.resource_group ASC")

        with connection.cursor() as cursor:
            if project_year:
                COMMON_QUERY = COMMON_QUERY + YEAR_QUERY
                sqlParameters.append(project_year.upper())
            if project_name:
                COMMON_QUERY = COMMON_QUERY + NAME_QUERY
                sqlParameters.append(project_name.upper() + "%")
            if resource:
                COMMON_QUERY = COMMON_QUERY + RESOURCE_QUERY
                sqlParameters.append(resource)

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
            "project_year",
            "project_name",
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
            "resource_group",
            "div_group"
        ],
    )
    result = [nt_result(*row) for row in cursor.fetchall()]
    result = [
        {
            "id": r.id,
            "project_year": r.project_year,
            "project_name": r.project_name,
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
            "resource_group": r.resource_group,
            "div_group": r.div_group
        }
        for r in result
    ]
    return result
