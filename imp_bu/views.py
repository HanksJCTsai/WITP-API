from collections import namedtuple
from os import name
from django.db import connection
from imp_bg.serializers import ImpBgSerializer
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .models import ImpBu
from .serializers import ImpBuSerializer

# Create your views here.


class ImpBuViewSet(viewsets.ModelViewSet):
    serializer_class = ImpBuSerializer
    queryset = ImpBu.objects.filter()

    def get_permissions(self):
        # 決定哪些method需要哪些認證
        # GET不用
        if self.request.method in ["POST","PUT","PATCH","DELETE"]:
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.AllowAny()]

    @action(detail=False, methods=["post"], name="query by bu")
    # API Format {"bu":"string"}
    def query_bu(self, request, pk=None):
        req = request.data
        bu: str = req.get("bu")
        bg_id = req.get("bg_id")
        bo_id = req.get("bo_id")
        COMMON_QUERY = "SELECT U.id, U.bu, U.bg_id, G.bg, U.bo_id, O.bo FROM imp_bu U, imp_bg G, imp_bo O WHERE (U.bo_id = O.id AND U.bg_id=G.id) "
        BU_QUERY = "AND UPPER(U.bu) LIKE UPPER (%s)"
        BOID_QUERY = "AND U.bo_id = %s"
        BGID_QUERY = "AND U.bg_id = %s"
        SORT_QUERY = "ORDER BY U.bu, G.bg, O.bo ASC"
        with connection.cursor() as cursor:
            if bu and bg_id > 0 and bo_id > 0:
                cursor.execute(
                    COMMON_QUERY + BU_QUERY + BOID_QUERY + BGID_QUERY + SORT_QUERY,
                    ["%" + bu + "%", bo_id, bg_id],
                )
            elif not bg_id > 0 and bo_id >0 and bu:
                cursor.execute(
                    COMMON_QUERY + BU_QUERY + BOID_QUERY + SORT_QUERY,
                    ["%" + bu + "%", bo_id],
                )
            elif not bo_id > 0 and bg_id > 0 and bu:
                cursor.execute(
                    COMMON_QUERY + BU_QUERY + BGID_QUERY + SORT_QUERY,
                    ["%" + bu + "%", bg_id],
                )
            elif not bu and bo_id > 0 and bg_id > 0:
                cursor.execute(
                    COMMON_QUERY + BOID_QUERY + BGID_QUERY + SORT_QUERY,
                    [bo_id, bg_id],
                )
            elif not bu and not bo_id > 0 and bg_id > 0:
                cursor.execute(
                    COMMON_QUERY + BGID_QUERY + SORT_QUERY,
                    [bg_id],
                )
            elif not bo_id > 0 and not bg_id > 0 and bu:
                cursor.execute(
                    COMMON_QUERY + BU_QUERY + SORT_QUERY,
                    ["%" + bu + "%"],
                )
            elif not bu and not bg_id > 0 and bo_id > 0:
                cursor.execute(
                    COMMON_QUERY + BOID_QUERY + SORT_QUERY,
                    [bo_id],
                )
            else:
                cursor.execute(
                    COMMON_QUERY + SORT_QUERY
                )

            result = namedtuplefetchall(cursor)
            return Response(result)


def namedtuplefetchall(cursor):
    # Return all rows from a cursor as a namedtuple
    # desc = cursor.description
    nt_result = namedtuple("Result", ["id", "bu", "bg_id", "bg", "bo_id", "bo"])
    result = [nt_result(*row) for row in cursor.fetchall()]
    result = [
        {
            "id": r.id,
            "bu": r.bu,
            "bg_id": r.bg_id,
            "bg": r.bg,
            "bo_id": r.bo_id,
            "bo": r.bo,
        }
        for r in result
    ]
    return result
