import json
from django.http import JsonResponse
from rest_framework import permissions, viewsets
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from django.core import serializers

from .models import ImpIbln
from .serializers import ImpIblnSerializer
from django.db.models import Q
# Create your views here.

class ImpIblnViewSet(viewsets.ModelViewSet):
    serializer_class = ImpIblnSerializer
    queryset = ImpIbln.objects.filter()

    def get_permissions(self):
        # 決定哪些method需要哪些認證
        # GET不用
        if self.request.method in ["POST","PUT","PATCH","DELETE"]:
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.AllowAny()]
    @swagger_auto_schema(
        method='post',
        operation_summary='Get ib detail data by project year, name, ib id',
        operation_description="Get ib detail data by project year, name, ib id",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "project_year": openapi.Schema(type=openapi.TYPE_STRING, description="IB Project Year"),
                "project_name": openapi.Schema(type=openapi.TYPE_STRING, description="IB Project"),
                "ib_id": openapi.Schema(type=openapi.TYPE_STRING, description="IB id"),
            },
            required=["project_year","project_name","ib_id"]
        ),
    )
    @action(detail=False, methods=["post"])
    def query_iblns(self, request, pk=None):
        try:
            data = {"code": 0, "msg": "", "data": " "}
            req = request.data
            project_year = req.get("project_year")
            project_name = req.get("project_name")
            ib_code = req.get("ib_id")
            result = ImpIbln.objects.filter(Q(ib_id=ib_code) & Q(project_name=project_name) & Q(project_year=project_year))
            data["code"] = 1
            data["msg"] = "Get Ib Detail data by ib id or project year or project name"
            data["data"] = json.loads(serializers.serialize("json", result))
            return JsonResponse(data)
        except Exception as e:
            data["code"] = 2
            data["msg"] = "Error message:" + str(e)
            data["data"] = json.loads(serializers.serialize("json", {}))
            return JsonResponse(data)
