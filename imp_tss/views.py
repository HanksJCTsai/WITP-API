from http import client
from itertools import count
from locale import currency
from django.http import JsonResponse
from django.db import connection
from django.conf import settings
from rest_framework.decorators import action
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from collections import namedtuple

from imp_tsspast.serializers import ImpTssPastSerializer

from .models import ImpTss
from .serializers import ImpTssSerializer
from imp_tsspast.models import ImpTssPast
from imp_cal.models import ImpCal
from imp_dept.models import ImpDept
from imp_div.models import ImpDiv
from imp_extnames.models import extnames

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import json
from django.db.models import Q,Sum
from django.core import serializers
from django.core.paginator import Paginator
import datetime
import time
import pandas as pd

# import MQTT by paho-mqtt
import paho.mqtt.publish as MQTTPublish
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
# Create your views here.
# Create your views here.


class ImpTssViewSet(viewsets.ModelViewSet):
    serializer_class = ImpTssSerializer
    queryset = ImpTss.objects.filter()

    def get_permissions(self):
        # 決定哪些method需要哪些認證
        # GET不用
        if self.request.method in ["POST","PUT","PATCH","DELETE"]:
            return [permissions.IsAuthenticated()]
            #  return [permissions.AllowAny()]
        else:
            return [permissions.AllowAny()]

    @swagger_auto_schema(
        method="post",
        operation_summary="Provide project name and ib code from TSS data by upload",
        operation_description="Get project name and ib code from TSS upload: project_name, ib_code",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "project_name": openapi.Schema(type=openapi.TYPE_STRING, description="TSS project name"),
            }
        ),
    )
    @action(detail=False, methods=["post"])
    def provideTSS_ProjectName_IbCode(self, request, pk=None):
        sqlParameters = []
        req = request.data
        project_name = req.get("project_name")

        COMMON_QUERY = """SELECT DISTINCT TSS.pmcs_ib_project_name AS project_name, TSS.ib_code FROM imp_tss TSS WHERE 1=1 """
        PN_QUERY = "AND UPPER(TSS.pmcs_ib_project_name) LIKE UPPER(%s) "
        COMMON_ORDER = "ORDER BY TSS.pmcs_ib_project_name, TSS.ib_code ASC"

        with connection.cursor() as cursor:
            if project_name:
                COMMON_QUERY = COMMON_QUERY + PN_QUERY
                sqlParameters.append(project_name + "%")
            cursor.execute(COMMON_QUERY + COMMON_ORDER, sqlParameters)
            result = namedtuplefetchall_4_name_ibcode(cursor)
            return Response(result)

    #獲取excel API並存儲數據
    @swagger_auto_schema(
        method='post',
        operation_summary="Update TSS by excel file",
        operation_description="TSS data from excel",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "file": openapi.Schema(type=openapi.TYPE_STRING, description="TSS excel file"),
            }
        ),
    )
    @action(detail=False,methods=["post"])
    def upload_excel_data(self, request):
        print("........................GET EXCEL........................")
        # get username from token by authtoken_token table's key
        userName = User.objects.get(id=(Token.objects.get(key=(request.META['HTTP_AUTHORIZATION'].split(' ',)[1])).user)).username
        data = {"code": 0,"msg": " ","data":" "}
        MQTTT_TOGGLE = settings.MQTTT_TOGGLE
        MQTT_HOST = settings.MQTT_HOST
        MQTT_PORT = settings.MQTT_PORT
        MQTT_TOPIC_SUCCESS = settings.MQTT_TOPICS["SUCCESS"].format(UserId =userName)
        MQTT_TOPIC_ERROR = settings.MQTT_TOPICS["ERROR"].format(UserId =userName)

        if self.request.method == "POST":
            e_file = self.request.FILES.get("file")
            if e_file is None:
                data["msg"] = "未上傳任何文件"
                publish_MQTT(MQTTT_TOGGLE, MQTT_TOPIC_ERROR, MQTT_HOST, MQTT_PORT, data["msg"])
                return JsonResponse(data)
            type_excel = e_file.name.split(".")[-1]
            if type_excel in ["xls","xlsx"]:
                startTime = time.time()
                #解析表
                try:
                    excel_data = pd.read_excel(e_file)
                except Exception as e:
                    data["msg"] = "文件解析失败"
                    publish_MQTT(MQTTT_TOGGLE, MQTT_TOPIC_ERROR, MQTT_HOST, MQTT_PORT, data["msg"])
                    return JsonResponse(data)
                excel_data_list = excel_data.values.tolist()
                # 對時間進行判斷,時間不是同一個月,抛出異常,
                date_month_list = []
                ib_code_list = []
                info_list = []
                for row in excel_data.iterrows():
                     date_month = str(row[1]["Date"])[:7]
                     ib_code = str(row[1]["Project Code"])
                     if ib_code not in ib_code_list:
                       ib_code_list.append(ib_code)
                     if date_month not in date_month_list:
                       date_month_list.append(date_month)
                       info = {}
                       info["Employee ID"] = str(row[1]["Employee ID"])
                       info["Name"] = str(row[1]["Name"])
                       info["Department"] = str(row[1]["Department"])
                       info["Project Code"] = str(row[1]["Project Code"])
                       info["Project Name"] = str(row[1]["Project Name"])
                       info["Project Leader"] = str(row[1]["Project Leader"])
                       info["Task Category"] = str(row[1]["Task Category"])
                       info["Task Item"] = str(row[1]["Task Item"])
                       info["Date"] = str(row[1]["Date"])
                       info["Working Hour"] = str(row[1]["Working Hour"])
                       info["Description"] = str(row[1]["Description"])
                       info["Tag"] = str(row[1]["Tag"])
                       info["Profit Center"] = str(row[1]["Profit Center"])
                       info["Charge Dept"] = str(row[1]["Charge Dept"])
                       info_list.append(info)
                if len(date_month_list) > 1:
                    data["code"] = -1
                    data["msg"] = "Data 不是同一個月份,無法上傳"
                    data["data"] = info_list
                    publish_MQTT(MQTTT_TOGGLE, MQTT_TOPIC_ERROR, MQTT_HOST, MQTT_PORT, data["msg"])
                    return JsonResponse(data)
                else:
                    project_year = str(date_month_list[0][0:4])
                    date_month = date_month_list[0]
                    month = str(date_month[5:7])
                     #根據 date_month 刪除tss中已存在的數據
                    ImpTss.objects.filter(profit_center_models__startswith=date_month,pmcs_ib_project_year=project_year).delete()
                    ImpTssPast.objects.filter(pmcs_ib_project_year=project_year,work_month=month).delete()
                #準備tsspast data
                df_tss_past_data = excel_data[["Name","Department","Project Code","Project Name","Project Leader","Working Hour"]].sort_values(by=["Project Code"],ascending=False)
                tss_list_to_insert = []
                for i in range(0,len(excel_data_list)):
                    impTss = ImpTss(
                        employee_id = excel_data_list[i][0],
                        employee_name = excel_data_list[i][1],
                        # department = excel_data_list[i][2],
                        department = transformNan(str(excel_data_list[i][2]),"nan"),
                        ib_code = excel_data_list[i][3],
                        pmcs_ib_project_name = excel_data_list[i][4],
                        project_leader = excel_data_list[i][5],
                        task_category = excel_data_list[i][6],
                        task_item =excel_data_list[i][7],
                        date = excel_data_list[i][8],
                        working_hour = excel_data_list[i][9],
                        description = excel_data_list[i][10],
                        tag = transformNan(str(excel_data_list[i][11]),"nan"),
                        profit_center_models = excel_data_list[i][8],
                        # profit_center = excel_data_list[i][12],
                        charge_dept = excel_data_list[i][13],
                        seq = excel_data_list[i][8],
                        #新增栏位
                        pmcs_ib_project_year = str(date_month_list[0][0:4]) #datetime.datetime.now().year,
                    )
                    tss_list_to_insert.append(impTss)
                ImpTss.objects.bulk_create(tss_list_to_insert)
                endTime = time.time()
                print("......................................",endTime - startTime)
                data["code"] = 1
                data["msg"] = "文件上傳成功"

                project_year = date_month_list[0][0:4]
                try:
                    print("........................START TSSPAST........................")
                    startTime = time.time()
                    df_tsspast_data = handle_tsspast_data(df_tss_past_data)
                    add_data_to_tsspast(df_tsspast_data,date_month_list[0][5:],project_year)
                    endTime = time.time()
                    print("......................................",endTime - startTime)
                except Exception as e:
                    data["code"] = 0
                    data["msg"] = str(e)
                    publish_MQTT(MQTTT_TOGGLE, MQTT_TOPIC_ERROR, MQTT_HOST, MQTT_PORT, data["msg"])
                    return JsonResponse(data)

                publish_MQTT(MQTTT_TOGGLE, MQTT_TOPIC_SUCCESS, MQTT_HOST, MQTT_PORT, data["msg"])
                return JsonResponse(data)
            else:
                data["msg"] = "文件类型错误"
                publish_MQTT(MQTTT_TOGGLE, MQTT_TOPIC_ERROR, MQTT_HOST, MQTT_PORT, data["msg"])
                return JsonResponse(data)
        else:
             data["msg"] = "上傳異常"
             publish_MQTT(MQTTT_TOGGLE, MQTT_TOPIC_ERROR, MQTT_HOST, MQTT_PORT, data["msg"])
             return JsonResponse(data)


    #查詢歷史數據
    @action(detail=False,methods=["post"])
    def find_page_data_by_keywords(self,request,pk=None):
        data = {"code": 0,"msg": " ","data": []}
        try:
            print("start.....")
            req = request.data
            page_size = req.get("page_size")
            current_page = req.get("current_page")
            project_name = req.get("pmcs_ib_project_name")
            # 查詢
            impTss_l = []
            if str(project_name).isspace():
                data["code"] = 0
                data["msg"] = "查詢參數必須填寫,不能爲空"
                return JsonResponse(data)
            print("............................2")
            impTss_l = ImpTss.objects.filter(Q(pmcs_ib_project_name__iexact=project_name))
            if len(impTss_l) == 0:
                print("............................3")
                data["msg"] = "未查詢到數據"
                return JsonResponse(data)
            else:
                #分頁
                paginator = Paginator(impTss_l,page_size)
                #獲取當前页码的数据
                page_data = paginator.page(current_page)
                #獲取總頁數
                total_page = paginator.num_pages

                #數據結果整理
                res = json.loads(serializers.serialize("json",page_data))
                context = {
                    "impTss_list": res,
                    "current_page": current_page,
                    "total_page": total_page,
                    "total_count": len(list(impTss_l))
                }
                data["code"] = 1
                data["msg"] = "查詢成功"
                data["data"] = context
                return JsonResponse(data)
        except Exception as e:
            data["msg"] = "系統異常,請稍後查詢"
            print(".........exception.............",e)
            return JsonResponse(data)

    #初始化數據
    @action(detail=False,methods=['post'])
    def find_page(self,request):
        data = {"code": 0,"msg": " ","data": []}
        req = request.data
        page_size = req.get("page_size")
        current_page = req.get("current_page")
        try:
            impTss_l = ImpTss.objects.all()
        except Exception as e:
            data["code"] = 1
            data["msg"] = "系统异常,请稍后查询"
            print("............................",e)
            return JsonResponse(data)
        paginator = Paginator(impTss_l,page_size)
        toatal_page = paginator.num_pages
        page_data =  paginator.page(current_page)
        res = json.loads(serializers.serialize("json",page_data))
        context = {"result":res,"curent_page":current_page,"total_page":toatal_page}
        print(context)
        return JsonResponse(context,safe=False)

    @action(detail=False,methods=["post"])
    def update_Tss(self,request,pk=None):
        data = {"code": 0,"msg": " ","data": []}
        json_dict = json.loads(self.request.body.decode())
        print(".......................",json_dict)
        update_id = json_dict.get("id")
        print("......................",update_id)
        update_employee_id = json_dict.get("employee_id")
        print("..................",update_employee_id)
        update_name = json_dict.get("employee_name")
        update_department = json_dict.get("department")
        update_ib_code = json_dict.get("ib_code")
        update_pmcs_ib_project_name = json_dict.get("pmcs_ib_project_name")
        update_project_leader = json_dict.get("project_leader")
        update_task_category = json_dict.get("task_category")
        update_task_item = json_dict.get("task_item")
        update_date = json_dict.get("date")
        update_working_hour = json_dict.get("working_hour")
        update_description = json_dict.get("description")
        update_tag = json_dict.get("tag")
        update_profit_center = json_dict.get("profit_center")
        update_charge_dept = json_dict.get("charge_dept")
        month_time = str(update_date)[5:7]
        try:
            print("start to update.......")
            #TODO
            tss = ImpTss.objects.filter(id=update_id).first()
            div_group = find_div_group_by_department(update_department,update_name)
            #修改tss_past數據
            update_tsspast_data(tss,json_dict,div_group,month_time)
            impTss = ImpTss.objects.filter(id = update_id).update(
                employee_id=update_employee_id,
                employee_name=update_name,
                department=update_department,
                ib_code=update_ib_code,
                pmcs_ib_project_name=update_pmcs_ib_project_name,
                project_leader=update_project_leader,
                task_category=update_task_category,
                date=update_date,
                task_item=update_task_item,
                working_hour=update_working_hour,
                description=update_description,
                tag=update_tag,
                profit_center=update_profit_center,
                charge_dept=update_charge_dept
                )
            #插入新的數據到DB
            # insert_data_to_tsspast(update_ib_code,month_time,update_project_year)
            data["code"] = 1
            data["msg"] = "數據修改成功"
            data["date"] = impTss
            return JsonResponse(data)
        except Exception as e:
            print("exception...............",e)
            data["msg"] = "數據修改失敗"
            return JsonResponse(data)


    @action(detail=False,methods=["delete"])
    # @action(detail=False,methods=["delete"],url_path="delete_Tss/(?P<id>[^/S+]+)")
    def delete_Tss(self,request,pk=None):
        data = {"code": 0,"msg": " ","data": []}
        # req = request.data
        # delete_id = req.get("id")
        delete_id = self.request.GET.get("id")
        tss = ImpTss.objects.filter(id=delete_id).first()
        try:
           #修改tsspast data
           update_tsspast_by_deletetss(tss)
           result = ImpTss.objects.get(id=delete_id).delete()
           data["code"] = 1
           data["msg"] = "刪除成功"
           data["data"] = result
           return JsonResponse(data)
        except Exception as e:
           data["msg"] = "刪除失敗"
           return JsonResponse(data)

    @swagger_auto_schema(
        method="post",
        operation_summary="Query upload TSS data",
        operation_description="Query upload TSS data by project_year, project_name, employee_name, employee_id, department, ib_code",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "project_year": openapi.Schema(type=openapi.TYPE_STRING, description="TSS' project year"),
                "project_name": openapi.Schema(type=openapi.TYPE_STRING, description="TSS' project name"),
                "employee_name": openapi.Schema(type=openapi.TYPE_STRING, description="TSS' project employee name"),
                "employee_id": openapi.Schema(type=openapi.TYPE_STRING, description="TSS' project employee id"),
                "department": openapi.Schema(type=openapi.TYPE_STRING, description="TSS' project department"),
                "ib_code": openapi.Schema(type=openapi.TYPE_STRING, description="TSS' project ib code"),
            }
        ),
    )
    @action(detail=False, methods=["post"])
    def query_tss(self, request, pk=None):
        sqlParameters = []
        req = request.data
        project_year = req.get("project_year")
        project_name = req.get("project_name")
        employee_name = req.get("employee_name")
        employee_id = req.get("employee_id")
        department = req.get("department")
        ib_code = req.get("ib_code")

        COMMON_QUERY = """SELECT TSS.id, TSS.pmcs_ib_project_year, TSS.pmcs_ib_project_name, TSS.employee_id, TSS.employee_name, TSS.department, TSS.ib_code, TSS.project_leader, TSS.task_category,
TSS.task_item, TSS.date, TSS.working_hour, TSS.tag, TSS.profit_center_models, TSS.seq, TSS.charge_dept, TSS.profit_center, TSS.description
FROM imp_tss TSS WHERE 1=1 """
        PY_QUERY = "AND UPPER(TSS.pmcs_ib_project_year) = UPPER(%s) "
        PN_QUERY = "AND UPPER(TSS.pmcs_ib_project_name) LIKE UPPER(%s) "
        EN_QUERY = "AND UPPER(TSS.employee_name) LIKE UPPER (%s) "
        EI_QUERY = "AND UPPER(TSS.employee_id) LIKE UPPER (%s) "
        DT_QUERY = "AND UPPER(TSS.department) LIKE UPPER (%s) "
        IB_QUERY = "AND TSS.ib_code = %s "
        COMMON_ORDER = "ORDER BY TSS.pmcs_ib_project_year, TSS.pmcs_ib_project_name, TSS.ib_code, TSS.project_leader, TSS.task_category, TSS.task_item, TSS.date ASC"

        with connection.cursor() as cursor:
            if project_year:
                COMMON_QUERY = COMMON_QUERY + PY_QUERY
                sqlParameters.append(project_year)
            if project_name:
                COMMON_QUERY = COMMON_QUERY + PN_QUERY
                sqlParameters.append(project_name + "%")
            if employee_name:
                COMMON_QUERY = COMMON_QUERY + EN_QUERY
                sqlParameters.append("%" + employee_name + "%")
            if employee_id:
                COMMON_QUERY = COMMON_QUERY + EI_QUERY
                sqlParameters.append("%" + employee_id + "%")
            if department:
                COMMON_QUERY = COMMON_QUERY + DT_QUERY
                sqlParameters.append("%" + department + "%")
            if ib_code:
                COMMON_QUERY = COMMON_QUERY + IB_QUERY
                sqlParameters.append("%" + ib_code + "%")

            cursor.execute(COMMON_QUERY + COMMON_ORDER, sqlParameters)

            result = namedtuplefetchall(cursor)
            return Response(result)

def namedtuplefetchall_4_name_ibcode(cursor):
    # Return all rows from a cursor as a namedtuple
    # desc = cursor.description
    nt_result = namedtuple(
        "Result",
        [
            "project_name",
            "ib_code",
        ],
    )
    result = [nt_result(*row) for row in cursor.fetchall()]
    result = [
        {
            "project_name": r.project_name,
            "ib_code": r.ib_code,
        }
        for r in result
    ]
    return result

def namedtuplefetchall(cursor):
    # Return all rows from a cursor as a namedtuple
    # desc = cursor.description
    nt_result = namedtuple(
        "Result",
        [
            "id",
            "pmcs_ib_project_year",
            "pmcs_ib_project_name",
            "employee_id",
            "employee_name",
            "department",
            "ib_code",
            "project_leader",
            "task_category",
            "task_item",
            "date",
            "working_hour",
            "tag",
            "profit_center_models",
            "seq",
            "charge_dept",
            "profit_center",
            "description"
        ],
    )
    result = [nt_result(*row) for row in cursor.fetchall()]
    result = [
        {
            "id": r.id,
            "pmcs_ib_project_year": r.pmcs_ib_project_year,
            "pmcs_ib_project_name": r.pmcs_ib_project_name,
            "employee_id": r.employee_id,
            "employee_name": r.employee_name,
            "department": r.department,
            "ib_code": r.ib_code,
            "project_leader": r.project_leader,
            "task_category": r.task_category,
            "task_item": r.task_item,
            "date": r.date,
            "working_hour": r.working_hour,
            "tag": r.tag,
            "profit_center_models": r.profit_center_models,
            "seq": r.seq,
            "charge_dept": r.charge_dept,
            "profit_center": r.profit_center,
            "description": r.description
        }
        for r in result
    ]
    return result

def update_tsspast_by_deletetss(tss):
    print(".......................")
    tss_month = str(tss.date)[5:7]
    tss_div_group = find_div_group_by_department(tss.department,tss.employee_name)
    tss_work_hour = tss.working_hour
    tss_ib_code = tss.ib_code
    tss_project_year = tss.pmcs_ib_project_year
    tss_project_name = tss.pmcs_ib_project_name
    #查詢tsspast
    tsspast = ImpTssPast.objects.filter(ib_code=tss_ib_code,
                                        div_group=tss_div_group,
                                        work_month=tss_month,
                                        pmcs_ib_project_name=tss_project_name,
                                        pmcs_ib_project_year=tss_project_year
                                        ).first()
    tsspast_work_hours = tsspast.work_hours #100
    total_hours = tsspast_work_hours - tss_work_hour
    working_days = ImpCal.objects.filter(month=tss_month).values("days").first()
    #算出tss_mm
    stander_working_hours = 6.5 * int(working_days.get("days"))
    tss_mm = round(total_hours/stander_working_hours,2)
    #修改tsspast data
    ImpTssPast.objects.filter(id=tsspast.id).update(
                                                            work_hours = total_hours,
                                                            tss_mm = tss_mm
                                                            )
def handle_tsspast_data(df_tss_past_data):
    #excel_data[["div_group","Project Code","Project Name","Project Leader","Working Hour"]]
    print("........handle tss_past_data........")
    # get deprtment for get division group
    dept_div_all_list = list(ImpDept.objects.all())
    extnames_div_all_list = list(extnames.objects.all())
    total_result = []
    result_dict = {}
    for row in df_tss_past_data.iterrows():
        employee_name = row[1]["Name"]
        ib_code = row[1]["Project Code"]
        working_hour = row[1]["Working Hour"]
        project_name = row[1]["Project Name"]
        department = row[1]["Department"]
        project_leader = row[1]["Project Leader"]
        if department:
            currency_div = list(filter(lambda x: x.dept == department , dept_div_all_list))
            if len(currency_div) > 0:
                div_group = ((currency_div)[0]).div.div_group
            else:
                print("*********Department:",department)
                count
        else:
            currency_div = list(filter( lambda x: x.emp_name == employee_name , extnames_div_all_list))
            if len(currency_div) > 0:
                div_group = ((currency_div)[0]).div.div_group
            else:
                print("*********Department:",department)
                count

        div_group = str(div_group) + "*" + str(ib_code)  + "*" + str(project_name) + "*" + str(project_leader)
        if div_group in result_dict.keys():
            result_dict[div_group] += working_hour
        else:
            result_dict[div_group] = working_hour

    for key in result_dict.keys():
        a = str(key).split("*")
        a.append(result_dict[key])
        total_result.append(a)
    return total_result

def get_department_list_by_div_group(div_group):
    div_id = ImpDiv.objects.filter(div_group=div_group).values("id").first().get("id")
    department_list = ImpDept.objects.filter(div_id=div_id).values_list().get("id")
    return department_list


def update_tsspast_data(tss,json_dict,div_group,month_time):
    tss_month = str(tss.date)[5:7]
    tss_div_group = find_div_group_by_department(tss.department,tss.employee_name)
    print(".............tss_div_group......",tss_div_group)
    tss_work_hour = tss.working_hour
    tss_ib_code = tss.ib_code
    tss_project_year = tss.pmcs_ib_project_year
    tss_project_name = tss.pmcs_ib_project_name
    #已存在的tsspast
    tsspast1 = ImpTssPast.objects.filter(ib_code=tss_ib_code,
                                         div_group=tss_div_group,
                                         work_month=tss_month,
                                         pmcs_ib_project_name=tss_project_name,
                                         pmcs_ib_project_year=tss_project_year
                                        ).first()
    print(".............imptsspast1......",tsspast1)
    #不確定存在的tsspast
    tsspast2 = ImpTssPast.objects.filter(
                                        ib_code=tss_ib_code,
                                        div_group=div_group,
                                        work_month=month_time,
                                        pmcs_ib_project_name=tss_project_name,
                                        pmcs_ib_project_year=tss_project_year
                                        ).first()
    print(".............imptsspast2......",tsspast2)

    if tss_month == month_time and tss_div_group == div_group and tss_work_hour == json_dict.get("working_hour") and tss_ib_code == json_dict.get("ib_code"):
        pass
    elif tss_month == month_time and tss_div_group == div_group and tss_work_hour != json_dict.get("working_hour") and tss_ib_code == json_dict.get("ib_code"):
        tsspast_work_hours = tsspast1.work_hours
        #對total_hours重新計算
        total_hours = tsspast_work_hours - tss_work_hour + float(json_dict.get("working_hour"))
        #根據month查詢出當月工作天數
        working_days = ImpCal.objects.filter(month=tss_month).values("days").first()
        #算出tss_mm
        stander_working_hours = 6.5 * int(working_days.get("days"))
        tss_mm = round(total_hours/stander_working_hours,2)
        #跟新操作
        ImpTssPast.objects.filter(id=tsspast1.id).update(
                                                         work_hours = total_hours,
                                                         tss_mm = tss_mm
                                                         )
    elif tss_month == month_time and tss_div_group != div_group:
        print("...")
        #判斷
        if tsspast2 is None:
            working_days = ImpCal.objects.filter(month=tss_month).values("days").first()
            #算出tss_mm
            print(".............imptsspast2 is None......")
            stander_working_hours = 6.5 * int(working_days.get("days"))
            tss_mm = round(float(json_dict.get("working_hour"))/stander_working_hours,2)
            ImpTssPast.objects.create(
                                      pmcs_ib_project_year=tss.pmcs_ib_project_year,
                                      pmcs_ib_project_name=json_dict.get("pmcs_ib_project_name"),
                                      work_month=tss_month,
                                      ib_code=json_dict.get("ib_code"),
                                      it_pm=json_dict.get("project_leader"),
                                      days=working_days.get("days"),
                                      tss_mm=tss_mm,
                                      work_hours=json_dict.get("working_hour"),
                                      div_group=div_group)

            total_hours1 = tsspast1.work_hours - float(json_dict.get("working_hour"))
            tss_mm1 = round(total_hours1/stander_working_hours,2)
            ImpTssPast.objects.filter(id=tsspast1.id).update(
                work_hours = total_hours1,
                tss_mm = tss_mm1
            )
        else:
            print(".............imptsspast2 no None......")
            total_hours1 = tsspast1.work_hours - float(json_dict.get("working_hour"))
            total_hours2 = tsspast2.work_hours + float(json_dict.get("working_hour"))
            working_days = ImpCal.objects.filter(month=tss_month).values("days").first()
            #算出tss_mm
            stander_working_hours = 6.5 * int(working_days.get("days"))
            tss_mm1 = round(total_hours1/stander_working_hours,2)
            tss_mm2 = round(total_hours2/stander_working_hours,2)
            ImpTssPast.objects.filter(id=tsspast1.id).update(
                                                                work_hours = total_hours1,
                                                                tss_mm = tss_mm1
                                                              )
            ImpTssPast.objects.filter(id=tsspast2.id).update(
                                                                work_hours = total_hours2,
                                                                tss_mm = tss_mm2
                                                              )

    print()

# def update_tsspast_data(impTss,ib_code,div_group,time_month,project_year,project_name,update_working_hour):
#     #刪除tsspast原來的數據
#     tsspast = ImpTssPast.objects.filter(ib_code=ib_code,
#                                         div_group=div_group,
#                                         work_month=time_month,
#                                         pmcs_ib_project_year=project_year,
#                                         pmcs_ib_project_name=project_name
#                                         ).first()
#     #impTss的project_name 與update_project_name
#     # delete_tsspast(project_year,project_name,ib_code,div_group,time_month)
#     # department_list = get_department_list_by_div_group(div_group)
#     total_working_hours = tsspast.get("work_hours") + skip_hour
#     id = tsspast.get("id")
#     # total_working_hours = 0
    # for department in department_list:
    #     working_hours = ImpTss.objects.filter(ib_code=ib_code,
    #                                          department=department,
    #                                        ).values("working_hour").aggregate(Sum("working_hour"))
    #     total_working_hours += working_hours
    # working_days = ImpCal.objects.filter(month=time_month).values("days").first()
    #算出tss_mm
#     stander_working_hours = 6.5 * int(working_days.get("days"))
#     tss_mm = round(total_working_hours/stander_working_hours,2)
#     it_pm = get_it_pm(ib_code,project_year)
#     impTsspast = ImpTssPast(
#            pmcs_ib_project_year=project_year,
#            pmcs_ib_project_name=project_name,
#            ib_code=ib_code,
#            it_pm=it_pm,
#            div_group=div_group,
#            work_month=time_month,
#            work_hours=total_working_hours,
#            days=working_days.get("days"),
#            tss_mm=tss_mm,
#         )
#     impTsspast.save()

#df_tsspast_data為DataFrame類型數據 pd.DataFrame(tatol_result,index=None,columns=["department","ib_code","working_hours"])
def add_data_to_tsspast(df_tsspast_data,time_month,project_year):
    try:
        df_tsspast_data_ = pd.DataFrame(df_tsspast_data,index=None,columns=["div_group","ib_code","project_name","project_leader","working_hours"])
        print("**********************add_data_to_tsspast******************")
        #time_month的有效工作日
        working_days = (ImpCal.objects.filter(month=time_month).values("days").first()).get("days")
        #算出tss_mm
        stander_working_hours = 6.5 * int(working_days)
        tsspast_list = []
        for row in df_tsspast_data_.iterrows():
            project_name = row[1]["project_name"]
            working_total_hours = round(row[1]["working_hours"],2)
            tss_mm = round(working_total_hours/stander_working_hours,2)
            it_pm = row[1]["project_leader"]
            div_group = row[1]["div_group"]
            impTsspast = ImpTssPast(
                pmcs_ib_project_year=project_year,
                pmcs_ib_project_name=project_name,
                ib_code=row[1]["ib_code"],
                it_pm=it_pm,
                work_month=time_month,
                work_hours=working_total_hours,
                days=working_days,
                tss_mm=tss_mm,
                div_group=div_group,
            )
            tsspast_list.append(impTsspast)
        ImpTssPast.objects.bulk_create(tsspast_list)
    except Exception as e:
        print("*****",e)


def find_div_group_by_department(department,employee_name):
    print("..........find_div_group_by_department..............")
    div_group = ""
    if str(department).lower() == "nan" or department == " ":
        div_id = extnames.objects.filter(emp_name=employee_name).values("div_group_id").first().get("div_group_id")
        div_group = ImpDiv.objects.filter(id=div_id).values("div_group").first().get("div_group")
    else:
        div_id_dict = ImpDept.objects.filter(dept=department).values("div_id").first()
        if div_id_dict is None:
            div_id = extnames.objects.filter(emp_name=employee_name).values("div_group_id").first().get("div_group_id")
            div_group = ImpDiv.objects.filter(id=div_id).values("div_group").first().get("div_group")
        else:
            div_id = div_id_dict.get("div_id")
            div_group = ImpDiv.objects.filter(id=div_id).values("div_group").first().get("div_group")
    return div_group


#處理數據tss_past
# def insert_data_to_tsspast(ib_code_list,time_month,project_year):
#     tsspast_list = []
#     for i in range(len(ib_code_list)):
#         #獲取一個 project_leader
#         project_name = ImpTss.objects.filter(ib_code = ib_code_list[i],pmcs_ib_project_year=project_year).values("pmcs_ib_project_name").first().get("pmcs_ib_project_name")
#         working_total_hours_dict = ImpTss.objects.filter(ib_code = ib_code_list[i],pmcs_ib_project_year=project_year).values("working_hour").aggregate(Sum("working_hour"))
#         working_total_hours = working_total_hours_dict.get("working_hour__sum")
#         #time_month的有效工作日
#         working_days = ImpCal.objects.filter(month=time_month).values("days").first()
#         #算出tss_mm
#         stander_working_hours = 6.5 * int(working_days.get("days"))
#         tss_mm = round(working_total_hours/stander_working_hours,2)
#         it_pm = get_it_pm(ib_code_list[i],project_year)
#         #根據department獲取imp_div的div_group
#         #imp_tss---->imp_div_dept---->imp_div
#         div_group = get_div_group(ib_code_list[i],project_year)
#         impTsspast = ImpTssPast(
#             pmcs_ib_project_year=project_year,
#             pmcs_ib_project_name=project_name,
#             ib_code=ib_code_list[i],
#             it_pm=it_pm,
#             div_group=div_group,
#             work_month=time_month,
#             work_hours=working_total_hours,
#             days=working_days.get("days"),
#             tss_mm=tss_mm,
#         )
#         tsspast_list.append(impTsspast)
#     ImpTssPast.objects.bulk_create(tsspast_list)


#獲取working_days
def get_working_days(time_month):
    working_days = ImpCal.objects.filter(month=time_month).values("days").first().get("days")
    return working_days
#獲取div_id
# def get_div_group(ib_code,project_year):
#     #獲取department
#     department = ImpTss.objects.filter(ib_code = ib_code,pmcs_ib_project_year=project_year).values("department").first().get("department")
#     print(".........................",department)
#     div_id = ""
#     if department is None:
#         #獲取department is None
#         employee_name = ImpTss.objects.filter(ib_code = ib_code,pmcs_ib_project_year=project_year).values("employee_name").first().get("employee_name")
#         div_id = extnames.objects.filter(emp_name=employee_name).values("div_group_id").first().get("div_group_id")
#     else:
#         #根據departement取div_id
#         div_id = ImpDept.objects.filter(dept=department).values("div_id").first()
#         if div_id is None:
#              #獲取div_id is None
#              employee_name = ImpTss.objects.filter(ib_code = ib_code,pmcs_ib_project_year=project_year).values("employee_name").first().get("employee_name")
#              div_id = extnames.objects.filter(emp_name=employee_name).values("div_group_id").first().get("div_group_id")
#         else:
#             div_id = div_id.get("div_id")
#     div_group = ImpDiv.objects.filter(id=div_id).values("div_group").first().get("div_group")
#     print("...........div_group.............",div_group)
#     return div_group

def delete_tsspast(project_year,project_name,ib_code,div_group,time_month):
    print("start delete tsspast........")
    ImpTssPast.objects.filter(pmcs_ib_project_year=project_year,
                              pmcs_ib_project_name=project_name,
                              ib_code=ib_code,
                              div_group=div_group,
                              work_month=time_month).delete()

def publish_MQTT(mqtt_toggle, mqtt_topic, mqtt_host, mqtt_port, message):
    if mqtt_toggle :
        print("Publish message to MQTT")
        MQTTPublish.single(
            topic= mqtt_topic,
            payload= message,
            hostname= mqtt_host,
            port= mqtt_port)

def transformNan(a,b):
    if a == b:
        return " "
    else:
        return a
