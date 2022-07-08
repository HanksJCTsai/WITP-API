from collections import namedtuple
from os import name
from django.db import connection
from imp_bg.serializers import ImpBgSerializer
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .models import ImpBg
from .serializers import ImpBgSerializer

# Create your views here.


class ImpBgViewSet(viewsets.ModelViewSet):
    serializer_class = ImpBgSerializer
    queryset = ImpBg.objects.filter()

    def get_permissions(self):
        # 決定哪些method需要哪些認證
        # GET不用
        if self.request.method in ["POST","PUT","PATCH","DELETE"]:
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.AllowAny()]

    @action(detail=False, methods=["post"], name="query by bg")
    # API Format {"bg":"string","bo_id": number}
    def query_bg(self, request, pk=None):
        req = request.data
        bg: str = req.get("bg")
        bo_id = req.get("bo")
        COMMON_QUERY = "SELECT G.id, G.bg, G.bo_id, O.bo FROM imp_bg G, imp_bo O WHERE G.bo_id = O.id "
        BG_QUERY = "AND UPPER(G.bg) LIKE UPPER (%s)"
        BOID_QUERY = "AND G.bo_id = %s"
        SORT_QUERY = "ORDER BY G.bg, O.bo ASC"
        with connection.cursor() as cursor:
            if bg and bo_id > 0 :
                cursor.execute(
                    COMMON_QUERY + BG_QUERY + BOID_QUERY + SORT_QUERY,
                    ["%" + bg + "%", bo_id],
                )
            elif not bg and bo_id > 0:
                cursor.execute(
                    COMMON_QUERY + BOID_QUERY + SORT_QUERY,
                    [bo_id],
                )
            elif not bo_id > 0 and bg:
                cursor.execute(
                    COMMON_QUERY + BG_QUERY + SORT_QUERY,
                    ["%" + bg + "%"],
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
    nt_result = namedtuple("Result", ["id", "bg", "bo_id", "bo"])
    result = [nt_result(*row) for row in cursor.fetchall()]
    result = [{"id": r.id, "bg": r.bg, "bo_id": r.bo_id, "bo": r.bo} for r in result]
    return result
