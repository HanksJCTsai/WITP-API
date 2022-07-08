from django.db import connection
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from collections import namedtuple
from .models import Resource
from .serializers import ResourceSerializer

# Create your views here.


class ResourceViewSet(viewsets.ModelViewSet):
    serializer_class = ResourceSerializer
    queryset = Resource.objects.filter()

    def get_permissions(self):
        # 決定哪些method需要哪些認證
        # GET不用
        if self.request.method in ["POST","PUT","PATCH","DELETE"]:
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.AllowAny()]

    @action(detail=False, methods=["post"])
    def query_resource(self, request, pk=None):
        req = request.data
        resource_group = req.get("resource_group")
        div_group = req.get("div_group")
        COMMON_QUERY = "SELECT T.id, T.resource_group, T.division, T.location, T.system, T.remark, V.div_group, V.id AS div_id FROM imp_resource T, imp_div V WHERE T.div_group_id = V.id"
        COMMON_ORDER = " ORDER BY T.resource_group, V.div_group, T.division, T.location, T.system ASC"

        with connection.cursor() as cursor:
            if resource_group and div_group > 0:
                cursor.execute(
                    COMMON_QUERY
                    + " AND (UPPER(T.resource_group) LIKE UPPER(%s) AND V.id = %s)"
                    + COMMON_ORDER,
                    ["%" + resource_group + "%", div_group],
                )
            elif not resource_group and div_group:
                cursor.execute(
                    COMMON_QUERY
                    + " AND V.id = %s"
                    + COMMON_ORDER,
                    [div_group],
                )
            elif not div_group > 0 and resource_group:
                cursor.execute(
                    COMMON_QUERY
                    + " AND UPPER(T.resource_group) LIKE UPPER(%s)"
                    + COMMON_ORDER,
                    ["%" + resource_group + "%"],
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
    nt_result = namedtuple("Result", ["id", "resource_group", "division_nick_name","location", "system", "remark", "div_group", "div_group_id"])
    result = [nt_result(*row) for row in cursor.fetchall()]
    result = [
        {
            "id": r.id,
            "resource_group": r.resource_group,
            "location": r.location,
            "system": r.system,
            "remark":r.remark,
            "div_group": r.div_group,
            "div_id": r.div_group_id,
            "div_nickname":r.division_nick_name
        }
        for r in result
    ]
    return result
