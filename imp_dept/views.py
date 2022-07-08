from django.db import connection
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from collections import namedtuple
from .models import ImpDept
from .serializers import ImpDeptSerializer

# Create your views here.


class ImpDeptViewSet(viewsets.ModelViewSet):
    serializer_class = ImpDeptSerializer
    queryset = ImpDept.objects.filter()

    def get_permissions(self):
        # 決定哪些method需要哪些認證
        # GET不用
        if self.request.method in ["POST","PUT","PATCH","DELETE"]:
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.AllowAny()]

    @action(detail=False, methods=["post"])
    # API Format {"dept": "MLD", "div_code": ""}
    def query_dept(self, request, pk=None):
        req = request.data
        dept = req.get("dept")
        div_id = req.get("div")
        COMMON_QUERY = "SELECT T.id, T.dept, V.div, V.div_group, V.id AS div_id FROM imp_dept T, imp_div V WHERE T.div_id = V.id "
        COMMON_ORDER = " ORDER BY T.dept, V.div, V.div_group ASC"

        with connection.cursor() as cursor:
            if dept and div_id > 0:
                cursor.execute(
                    COMMON_QUERY
                    + " AND UPPER(T.dept) LIKE UPPER(%s) AND V.id = %s "
                    + COMMON_ORDER,
                    ["%" + dept + "%", div_id],
                )
            elif not dept and div_id > 0:
                cursor.execute(
                    COMMON_QUERY
                    + " AND V.id = %s "
                    + COMMON_ORDER,
                    [div_id],
                )
            elif not div_id > 0 and dept:
                cursor.execute(
                    COMMON_QUERY + " AND UPPER(T.dept) LIKE UPPER(%s) " + COMMON_ORDER,
                    ["%" + dept + "%"],
                )
            else:
                cursor.execute(
                    COMMON_QUERY + COMMON_ORDER,
                )

            result = namedtuplefetchall(cursor)
            return Response(result)


def namedtuplefetchall(cursor):
    # Return all rows from a cursor as a namedtuple
    # desc = cursor.description
    nt_result = namedtuple("Result", ["id", "dept", "div", "div_group", "div_id"])
    result = [nt_result(*row) for row in cursor.fetchall()]
    result = [
        {
            "id": r.id,
            "dept": r.dept,
            "div": r.div,
            "div_group": r.div_group,
            "div_id": r.div_id,
        }
        for r in result
    ]
    return result
