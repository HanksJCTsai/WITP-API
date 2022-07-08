from collections import namedtuple

from django.db import connection
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .models import extnames
from .serializers import ExtnamesSerializer

# Create your views here.
class ExtnamesViewSet(viewsets.ModelViewSet):
    serializer_class = ExtnamesSerializer
    queryset = extnames.objects.filter()

    def get_permissions(self):
        # 決定哪些method需要哪些認證
        # GET不用
        if self.request.method in ["POST","PUT","PATCH","DELETE"]:
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.AllowAny()]

    @action(detail=False, methods=["post"])
    # API Format {"emp_name": "", "div": "MLD0"}
    def query_name_div(self, request, pk=None):
        req = request.data
        emp_name = req.get("emp_name")
        div_code = req.get("div_group")
        with connection.cursor() as cursor:
            if not div_code > 0 and emp_name:
                cursor.execute(
                    "SELECT E.id, E.emp_name, E.div_group_id, D.div_group FROM imp_extnames E, imp_div D "
                    "WHERE E.div_group_id= D.id AND UPPER(E.emp_name) LIKE UPPER (%s) "
                    "ORDER BY E.emp_name, D.div_group ASC",
                    ["%" + emp_name + "%"],
                )
            elif not emp_name and div_code > 0:
                cursor.execute(
                    "SELECT E.id, E.emp_name, E.div_group_id, D.div_group FROM imp_extnames E, imp_div D "
                    "WHERE E.div_group_id = D.id AND D.id = %s "
                    "ORDER BY E.emp_name, D.div_group ASC",
                    [div_code],
                )
            elif emp_name and div_code > 0:
                cursor.execute(
                    "SELECT E.id, E.emp_name, E.div_group_id, D.div_group FROM imp_extnames E, imp_div D "
                    "WHERE E.div_group_id= D.id AND UPPER(E.emp_name) LIKE UPPER (%s) "
                    "AND D.id = %s ORDER BY E.emp_name, D.div_group ASC",
                    ["%" + emp_name + "%", div_code],
                )
            else:
                cursor.execute(
                    "SELECT E.id, E.emp_name, E.div_group_id, D.div_group FROM imp_extnames E, imp_div D "
                    "WHERE E.div_group_id = D.id ORDER BY E.emp_name, D.div_group ASC"
                )
            result = namedtuplefetchall(cursor)
            return Response(result)


def namedtuplefetchall(cursor):
    # Return all rows from a cursor as a namedtuple
    # desc = cursor.description
    nt_result = namedtuple("Result", ["id", "emp_name", "div_group_id", "div_group"])
    result = [nt_result(*row) for row in cursor.fetchall()]
    result = [
        {
            "id": r.id,
            "emp_name": r.emp_name,
            "div_id": r.div_group_id,
            "div_code": r.div_group,
        }
        for r in result
    ]
    return result
