from unittest import result
from django.http import JsonResponse
from rest_framework import permissions, viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from django.core import serializers
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from collections import namedtuple

from .models import Pajln
from .serializers import PajlnSerializer
from django.db.models import Q

# Create your views here.
from imp_ib.models import ImpIb
from imp_ibln.models import ImpIbln
from imp_tsspast.models import ImpTssPast
import datetime
import json


class PajlnViewSet(viewsets.ModelViewSet):
    serializer_class = PajlnSerializer
    queryset = Pajln.objects.filter()

    def get_permissions(self):
        # 決定哪些method需要哪些認證
        # GET不用
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.AllowAny()]

    @action(detail=False, methods=["post"])
    def delete_paj_man_month(self, request, pk=None):
        data = {"code": 0, "msg": " ", "data": ""}
        try:
            req = request.data
            delete_id = req.get("id")
            result = Pajln.objects.filter(id=delete_id).delete()
            data["msg"] = "删除成功"
            data["data"] = result
            data["code"] = 1
            return JsonResponse(data)
        except Exception as e:
            print("......刪除異常........", e)
            data["msg"] = "删除失敗"
            data["data"] = e
            return JsonResponse(data)

    @action(detail=False, methods=["post"])
    def add_paj_man_month(self, request, pk=None):
        data = {"code": 0, "msg": "", "data": " "}
        req = request.data
        ib_code = req.get("ib_code")
        project_year = req.get("project_year")
        project_name = req.get("project_name")
        try:
            pajln = Pajln(
                ib_code=req.get("ib_code"),
                jan_plan=handle_plan_data(req.get("jan_plan")),
                feb_plan=handle_plan_data(req.get("feb_plan")),
                mar_plan=handle_plan_data(req.get("mar_plan")),
                apr_plan=handle_plan_data(req.get("apr_plan")),
                may_plan=handle_plan_data(req.get("may_plan")),
                jun_plan=handle_plan_data(req.get("jun_plan")),
                jul_plan=handle_plan_data(req.get("jul_plan")),
                aug_plan=handle_plan_data(req.get("aug_plan")),
                sep_plan=handle_plan_data(req.get("sep_plan")),
                oct_plan=handle_plan_data(req.get("oct_plan")),
                nov_plan=handle_plan_data(req.get("nov_plan")),
                dec_plan=handle_plan_data(req.get("dec_plan")),
                jan_paj_no=req.get("jan_paj_no"),
                feb_paj_no=req.get("feb_paj_no"),
                mar_paj_no=req.get("mar_paj_no"),
                apr_paj_no=req.get("apr_paj_no"),
                may_paj_no=req.get("may_paj_no"),
                jun_paj_no=req.get("jun_paj_no"),
                jul_paj_no=req.get("jul_paj_no"),
                aug_paj_no=req.get("aug_paj_no"),
                sep_paj_no=req.get("sep_paj_no"),
                oct_paj_no=req.get("oct_paj_no"),
                nov_paj_no=req.get("nov_paj_no"),
                dec_paj_no=req.get("dec_paj_no"),
                div_group=req.get("div_group"),
                project_name=req.get("project_name"),
                project_year=req.get("project_year"),
                creater=req.get("creater"),
                creatdate= req.get("creatdate")
            )
            result = pajln.save()
            result = Pajln.objects.filter(Q(ib_code=ib_code) & Q(project_name=project_name) & Q(project_year=project_year))
            data["code"] = 1
            data["msg"] = "信息添加成功"
            data["data"] = json.loads(serializers.serialize("json", result))
            return JsonResponse(data)
        except Exception as e:
            print(".................添加異常...............", e)
            data["msg"] = "信息添加失敗"
            data["data"] = e
            return JsonResponse(data)

    @action(detail=False, methods=["post"])
    def update_paj_man_month(self, request, pk=None):
        print("............start to update data.........")
        data = {"code": 0, "msg": " ", "data": " "}
        req = request.data
        ib_code = req.get("ib_code")
        project_year = req.get("project_year")
        project_name = req.get("project_name")
        try:
            print("-----------------")
            update_id = req.get("id")
            result = Pajln.objects.filter(id=update_id).update(
                div_group=req.get("div_group"),
                jan_plan=req.get("jan_plan"),
                feb_plan=req.get("feb_plan"),
                mar_plan=req.get("mar_plan"),
                apr_plan=req.get("apr_plan"),
                may_plan=req.get("may_plan"),
                jun_plan=req.get("jun_plan"),
                jul_plan=req.get("jul_plan"),
                aug_plan=req.get("aug_plan"),
                sep_plan=req.get("sep_plan"),
                oct_plan=req.get("oct_plan"),
                nov_plan=req.get("nov_plan"),
                dec_plan=req.get("dec_plan"),
                jan_paj_no=req.get("jan_paj_no"),
                feb_paj_no=req.get("feb_paj_no"),
                mar_paj_no=req.get("mar_paj_no"),
                apr_paj_no=req.get("apr_paj_no"),
                may_paj_no=req.get("may_paj_no"),
                jun_paj_no=req.get("jun_paj_no"),
                jul_paj_no=req.get("jul_paj_no"),
                aug_paj_no=req.get("aug_paj_no"),
                sep_paj_no=req.get("sep_paj_no"),
                oct_paj_no=req.get("oct_paj_no"),
                nov_paj_no=req.get("nov_paj_no"),
                dec_paj_no=req.get("dec_paj_no"),
                updater=req.get("updater"),
                updatedate=req.get("updatedate"),
            )
            if result > 0 :
                result = Pajln.objects.filter(Q(ib_code=ib_code) & Q(project_name=project_name) & Q(project_year=project_year))
            data["msg"] = "信息修改成功"
            data["code"] = 1
            data["data"] = json.loads(serializers.serialize("json", result))
            return JsonResponse(data)
        except Exception as e:
            print(".......修改異常......", e)
            data["msg"] = "信息修改失敗"
            data["data"] = e
            return JsonResponse(data)

    """imp_pajln(generate paj data), imp_tss(Actual TSS data), imp_ib(ib data)"""

    @swagger_auto_schema(
        method='post',
        operation_summary="Query data for PAJ confirm",
        operation_description="Data from pajln, ib, ibln, tss",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "project_name": openapi.Schema(type=openapi.TYPE_STRING, description="IB project name"),
                "ib_code": openapi.Schema(type=openapi.TYPE_STRING, description="IB ib code"),
            }
        ),
    )
    @action(detail=False, methods=["post"])
    def get_data_from_pajln(self, request, pk=None):
        data = {"code": 0, "msg": " ", "data": ""}
        req = request.data
        project_name = req.get("project_name")
        ib_code = req.get("ib_code")
        project_year = datetime.datetime.now().year
        try:
            data["code"] = 1
            data["msg"] = "查詢成功"
            paJln = get_data_from_pajln_by_keywords(project_year, project_name, ib_code)
            tssPast = get_data_from_tss_by_keywords(project_year, project_name, ib_code)
            ib = get_data_from_ib_by_keywords(project_year, project_name, ib_code)
            ibLn = get_data_from_ibln_by_id(project_year, project_name, ib_code)
            result = {"data": data, "pajln": paJln, "tssPast": tssPast,"ib": ib, "ibLn": ibLn}
            return JsonResponse(result)
        except Exception as e:
            print("..............exception.....", e)
            data["msg"] = "查詢錯誤"
            return JsonResponse(data)

    @action(detail=False, methods=["post"])
    def download_pajln_data(self, request, pk=None):
        data = {"code": 0, "msg": " ", "data": " "}
        pajln_list = []
        req = request.data
        project_year = req.get("project_year")
        project_name = req.get("project_name")
        ib_code = req.get("ib_code")
        try:
            if len(project_year) > 0 and len(project_name) > 0 and len(ib_code) > 0:
                pajln_list = Pajln.objects.filter(
                    Q(project_year=project_year),
                    Q(project_name=project_name),
                    Q(ib_code=ib_code),
                ).values()
            elif len(project_year) > 0 and len(project_name) > 0:
                pajln_list = Pajln.objects.filter(
                    Q(project_year=project_year), Q(project_name=project_name)
                ).values()
            elif len(project_year) > 0 and len(ib_code) > 0:
                pajln_list = Pajln.objects.filter(
                    Q(project_year=project_year), Q(ib_code=ib_code)
                ).values()
            elif len(project_name) > 0 and len(ib_code) > 0:
                pajln_list = Pajln.objects.filter(
                    Q(project_name=project_name), Q(ib_code=ib_code)
                ).values()
            elif len(project_year) > 0:
                pajln_list = Pajln.objects.filter(Q(project_year=project_year)).values()
            elif len(project_name) > 0:
                pajln_list = Pajln.objects.filter(Q(project_name=project_name)).values()
            else:
                pajln_list = Pajln.objects.filter(Q(ib_code=ib_code)).values()
            if len(list(pajln_list)) == 0:
                data["msg"] = "未查詢到相關信息"
                data["data"] = ""
                return JsonResponse(data)
            print("...................", pajln_list)
            data["msg"] = "查詢成功"
            data["code"] = 1
            data["data"] = list(pajln_list)
            return JsonResponse(data)
        except Exception as e:
            data["msg"] = "查詢失敗"
            data["data"] = str(e)
            return JsonResponse(data)


def handle_plan_data(data):
    return data == 0 if data == "" else data


def get_data_from_ibln_by_id(project_year, project_name, ib_code):
    print("start query IBLN data............")
    ib_id = (
        ImpIb.objects.filter(Q(project_year=project_year), Q(project_name=project_name), Q(ib_code=ib_code))
        .values("id")
        .first()
        .get("id")
    )
    ibLn = ImpIbln.objects.filter(ib_id=ib_id)
    return json.loads(serializers.serialize("json", ibLn))

def get_data_from_ib_by_keywords(project_year, project_name, ib_code):
    print("start query IB data............")
    ib = ImpIb.objects.filter(Q(project_year=project_year), Q(project_name=project_name), Q(ib_code=ib_code))
    return json.loads(serializers.serialize("json", ib))

def get_data_from_pajln_by_keywords(project_year, project_name, ib_code):
    print(".............start query pajln data..................")
    pajln = Pajln.objects.filter(Q(project_year=project_year), Q(project_name=project_name), Q(ib_code=ib_code))
    return json.loads(serializers.serialize("json", pajln))

def get_data_from_tss_by_keywords(project_year, project_name, ib_code):
    print(".............start query tss data..................")
    tss_data = ImpTssPast.objects.filter(Q(pmcs_ib_project_year=project_year), Q(pmcs_ib_project_name=project_name), Q(ib_code=ib_code)).values("tss_mm", "div_group", "work_month")
    tsspast_dict = {}
    for tsspast in tss_data:
        print(".............start handle data..................")
        work_month = tsspast.get("work_month")
        div_group = tsspast.get("div_group")
        tss_mm = tsspast.get("tss_mm")
        # 月份處理
        tss_month = getMonthPlan(work_month)
        if div_group not in tsspast_dict.keys():
            print("....................")
            tsspast_dict[div_group] = {}
            tsspast_dict[div_group][tss_month] = tss_mm
        else:
            tsspast_dict[div_group][tss_month] = tss_mm
    return tsspast_dict


def getMonthPlan(tss_month):
    date_dict = {
        "01": "jan_tss",
        "02": "feb_tss",
        "03": "mar_tss",
        "04": "apr_tss",
        "05": "may_tss",
        "06": "jun_tss",
        "07": "jul_tss",
        "08": "aug_tss",
        "09": "sep_tss",
        "10": "oct_tss",
        "11": "nov_tss",
        "12": "dec_tss",
    }
    return date_dict.get(tss_month)
