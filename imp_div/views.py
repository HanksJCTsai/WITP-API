from django.db import connection
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from collections import namedtuple

from .models import ImpDiv
from .serializers import ImpDivSerializer

# Create your views here.


class ImpDivViewSet(viewsets.ModelViewSet):
    serializer_class = ImpDivSerializer
    queryset = ImpDiv.objects.filter()

    def get_permissions(self):
        # 決定哪些method需要哪些認證
        # GET不用
        if self.request.method in ["POST","PUT","PATCH","DELETE"]:
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.AllowAny()]

    @swagger_auto_schema(
        method='post',
        operation_summary="Query division data by div, div code, div functions",
        operation_description="Query division data by div, div code, div functions",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "div": openapi.Schema(type=openapi.TYPE_STRING, description="Division Nickname"),
                "div_code": openapi.Schema(type=openapi.TYPE_STRING, description="Division Code"),
                "functions": openapi.Schema(type=openapi.TYPE_STRING, description="Division Functions"),
            },
        ),
    )
    @action(detail=False, methods=["post"])
    def query_div(self, request, pk=None):
        req = request.data
        division = req.get("div")
        divisioncode = req.get("div_code")
        divisionfuns = req.get("functions")
        COMMON_QUERY = (
            "SELECT id, div_group, functions, div, rate FROM imp_div WHERE 1=1"
        )
        DIV_QUERY = "AND UPPER(div_group) LIKE UPPER (%s)"
        DIVCODE_QUERY = "AND UPPER(div) LIKE UPPER (%s)"
        DIVFUNS_QUERY = "AND UPPER(functions) LIKE UPPER (%s)"
        SORT_QUERY = "ORDER BY div, div_group, functions, rate ASC"
        with connection.cursor() as cursor:
            if division and divisioncode and divisionfuns:
                cursor.execute(
                    COMMON_QUERY
                    + DIV_QUERY
                    + DIVCODE_QUERY
                    + DIVFUNS_QUERY
                    + SORT_QUERY,
                    [
                        "%" + division + "%",
                        "%" + divisioncode + "%",
                        "%" + divisionfuns + "%",
                    ],
                )
            elif not division and divisioncode and divisionfuns:
                cursor.execute(
                    COMMON_QUERY + DIVCODE_QUERY + DIVFUNS_QUERY + SORT_QUERY,
                    ["%" + divisioncode + "%", "%" + divisionfuns + "%"],
                )
            elif division and not divisioncode and divisionfuns:
                cursor.execute(
                    COMMON_QUERY + DIV_QUERY + DIVFUNS_QUERY + SORT_QUERY,
                    ["%" + division + "%", "%" + divisionfuns + "%"],
                )
            elif division and divisioncode and not divisionfuns:
                cursor.execute(
                    COMMON_QUERY + DIV_QUERY + DIVCODE_QUERY + SORT_QUERY,
                    ["%" + division + "%", "%" + divisioncode + "%"],
                )
            elif not division and not divisioncode and divisionfuns:
                cursor.execute(
                    COMMON_QUERY + DIVFUNS_QUERY + SORT_QUERY,
                    ["%" + divisionfuns + "%"],
                )
            elif division and not divisioncode and not divisionfuns:
                cursor.execute(
                    COMMON_QUERY + DIV_QUERY + SORT_QUERY,
                    ["%" + division + "%"],
                )
            elif not division and divisioncode and not divisionfuns:
                cursor.execute(
                    COMMON_QUERY + DIVCODE_QUERY + SORT_QUERY,
                    ["%" + divisioncode + "%"],
                )
            else:
                cursor.execute(
                    COMMON_QUERY + SORT_QUERY,
                )

            result = namedtuplefetchall(cursor)
            return Response(result)


def namedtuplefetchall(cursor):
    # Return all rows from a cursor as a namedtuple
    # desc = cursor.description
    nt_result = namedtuple("Result", ["id", "div_group", "functions", "div", "rate"])
    result = [nt_result(*row) for row in cursor.fetchall()]
    result = [
        {
            "id": r.id,
            "div": r.div,
            "functions": r.functions,
            "div_group": r.div_group,
            "rate": r.rate,
        }
        for r in result
    ]
    return result
