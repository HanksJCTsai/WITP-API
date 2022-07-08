import datetime
from itertools import count
from tokenize import Number
from urllib import response
from django.http import JsonResponse
from rest_framework import permissions, viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.db import connection
from collections import namedtuple

from django.core import serializers
import json

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action

from .models import ImpCal
from .serializers import ImpCalSerializer

# Create your views here.


class ImpCalViewSet(viewsets.ModelViewSet):
    serializer_class = ImpCalSerializer
    queryset = ImpCal.objects.filter()

    def get_permissions(self):
        # 決定哪些method需要哪些認證
        # GET不用
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.AllowAny()]
    @swagger_auto_schema(
        method = "post",
        operation_summary= "Get work month for TSS_Cal maint",
        operation_description="Get work month for TSS_Cal maint",
            request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
            }
        )
    )
    @action(detail= False, methods= ["post"])
    def getWorkMonth(self, pk= None):
        response = {"code": 0,"message": "","data": []}
        try:
            months_lst = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            work_months = []
            for i in range(len(months_lst)):
                i = i + 1
                work_month = {
                    "key": int(i), "value": months_lst[i-1]
                }
                work_months.append(work_month)
            response["code"] = 1
            response["message"] = "Success!"
            response["data"] = work_months
            return JsonResponse(response)
        except Exception as e:
            response["code"] = 2
            response["message"] = "Get Resource Country error"
            response["data"] = e
            return JsonResponse(response)

    @swagger_auto_schema(
        method="post",
        operation_summary="Get resource country for TSS_Cal maint",
        operation_description="Get resource country for TSS_Cal maint",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "country": openapi.Schema(
                    type= openapi.TYPE_STRING,
                    description= "Countury where the resource is located"
                )
            }
        )
    )
    @action(detail= False, methods=["post"])
    def getResourceCountry(self, request, pk=None):
        response = {"code": 0,"message": "","data": []}
        try:
            conutry_source = []
            conutry_source.append({"key":1, "value":"TAIWAN"})
            conutry_source.append({"key":2, "value":"CHINA"})
            req = request.data
            resource_location = req.get("country")
            if resource_location :
                # Filter python objects with list comprehensions
                output_dict = [x for x in conutry_source if x["value"] == resource_location]
                response["code"] = 1
                response["message"] = "Success!"
                response["data"] = output_dict
                if len(output_dict) == 0:
                    response["message"] = "No data found!"
            else:
                response["code"] = 1
                response["message"] = "Success!"
                response["data"] = conutry_source
            return JsonResponse(response)
        except Exception as e:
            response["code"] = 2
            response["message"] = "Get Resource Country error"
            response["data"] = e
            return JsonResponse(response)


    @swagger_auto_schema(
        method="post",
        operation_summary="Query for TSS_Cal data",
        operation_description="Query for TSS_Cal data",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "country": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Project resource team's localtion",
                ),
                "year": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Project work's year"
                ),
                "month": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Project work's month"
                ),
                "days": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Project Work's days"
                ),
            },
            required=["country", "year", "month"],
        ),
    )
    @action(detail=False, methods=["post"])
    def query_cal(self, request, pk=None):
        sqlParameters = []
        req = request.data
        project_countury = req.get("country")
        project_year = req.get("year")
        project_month = req.get("month")

        COMMON_QUERY = """SELECT CAL.id, CAL.country, CAL.year, CAL.month, CAL.days, CAL.creater, CAL.creatdate, CAL.updater, CAL.updatedate FROM imp_cal CAL WHERE 1=1"""
        PC_QUERY = "AND UPPER(CAL.country) LIKE UPPER(%s) "
        PY_QUERY = "AND CAL.year = %s "
        PM_QUERY = "AND CAL.month = %s "
        COMMON_ORDER = "ORDER BY CAL.country, CAL.year, CAL.month, CAL.days ASC"

        with connection.cursor() as cursor:
            if project_countury:
                COMMON_QUERY = COMMON_QUERY + PC_QUERY
                sqlParameters.append("%" + project_countury + "%")
            if project_year:
                COMMON_QUERY = COMMON_QUERY + PY_QUERY
                sqlParameters.append(project_year)
            if project_month:
                COMMON_QUERY = COMMON_QUERY + PM_QUERY
                sqlParameters.append(project_month)

            cursor.execute(COMMON_QUERY + COMMON_ORDER, sqlParameters)
            results = namedtuplefetchall_IMPCal(cursor)
        return Response(results)

def namedtuplefetchall_IMPCal(cursor):
    # Return all rows from a cursor as a namedtuple
    # desc = cursor.description
    nt_result = namedtuple(
        "Result",
        [
            "id",
            "country",
            "year",
            "month",
            "days",
            "creater",
            "creatdate",
            "updater",
            "updatedate",
        ],
    )
    result = [nt_result(*row) for row in cursor.fetchall()]
    result = [
        {
            "id":r.id,
            "country": r.country,
            "year": r.year,
            "month": r.month,
            "days": r.days,
            "creatdate": r.creatdate,
            "creater": r.creater,
            "updatedate": r.updatedate,
            "updater": r.updater,
        }
        for r in result
    ]
    return result
