from django.http.response import HttpResponse
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from .models import ImpBo
from .serializers import ImpBoSerializer

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# Create your views here.


class ImpBoViewSet(viewsets.ModelViewSet):
    serializer_class = ImpBoSerializer
    queryset = ImpBo.objects.filter()

    def get_permissions(self):
        # 決定哪些method需要哪些認證
        # GET不用
        if self.request.method in ["POST","PUT","PATCH","DELETE"]:
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.AllowAny()]

    @swagger_auto_schema(
        method="post",
        operation_summary="Query BO data",
        operation_description="Query BO data by Bo name",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "bo": openapi.Schema(type=openapi.TYPE_STRING, description="Bo name")
            }
        ),
    )
    @action(detail=False, methods=["post"])
    def query_bo(self, request, pk=None):
        req = request.data
        bo = req.get("bo")
        queryset = ImpBo.objects.raw(
            "SELECT id, bo FROM imp_bo WHERE UPPER(bo) LIKE UPPER (%s) ORDER BY bo ASC",
            ["%" + bo + "%"],
        )
        serializer = ImpBoSerializer(queryset, many=True)
        return Response(serializer.data)
