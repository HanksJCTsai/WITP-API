from django.db import connection
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from collections import namedtuple
from datetime import datetime
from time import strftime
from fpdf import FPDF

from .models import ImpPrf
from .serializers import PrfSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import codecs
from django.utils.http import urlquote
from django.db.models import Q
import datetime
from .models import ImpPrf
from imp_ib.models import ImpIb
from .serializers import PrfSerializer
import pandas as pd
from imp_div.models import ImpDiv
from imp_pajln.models import Pajln
from imp_prfln.models import ImpPrfln
from imp_tsspast.models import ImpTssPast
from imp_ibln.models import ImpIbln
from io import BytesIO
# Create your views here.
class PrfViewSet(viewsets.ModelViewSet):
    serializer_class = PrfSerializer
    queryset = ImpPrf.objects.filter()

    def get_permissions(self):
        # 決定哪些method需要哪些認證
        # GET不用
        if self.request.method in ["POST","PUT", "PATCH", "DELETE"]:
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.AllowAny()]

    @action(detail=False, methods=["post"])
    def query_prf(self, request, pk=None):
        sqlParameters = []
        req = request.data
        project_year = req.get("project_year")
        project_name = req.get("project_name")
        it_pm = req.get("it_pm")
        site = req.get("site")
        # plan_date_star = req.get("plan_start")
        # plan_date_end = req.get("plan_finish")
        project_cate = req.get("project_category")
        project_type = req.get("project_type")
        bu = req.get("bu")
        handle_div = req.get("handle_div")
        cancel = req.get("cancelled")
        complete = req.get("complete")
        ib_code = req.get("ib_code")
        ep_code = req.get("ep_code")

        COMMON_QUERY = """SELECT PRF.id, PRF.project_year, PRF.project_name, PRF.it_pm, PRF.biz_owner, PRF.contact_window, PRF.customer, PRF.site,
PRF.plan_start, PRF.plan_finish, PRF.recv_ep_code, PRF.comments, PRF.cancelled, PRF.complete, PRF.bud_syst_recv_chg_dept, PRF.bu, PRF.bg, PRF.bo, PRF.handle_div, PRF.project_category, PRF.project_type, PRF.recv_chg_dept, PRF.mis_ib_code, PRF.mis_ep_code, PRF.creatdate, PRF.creater, PRF.updatedate, PRF.updater, '' AS prf_ln FROM imp_prf PRF WHERE 1=1 """
        PY_QUERY = "AND UPPER(PRF.project_year) = UPPER(%s) "
        PN_QUERY = "AND UPPER(PRF.project_name) LIKE UPPER(%s) "
        IP_QUERY = "AND UPPER(PRF.it_pm) LIKE UPPER (%s) "
        SITE_QUERY = "AND UPPER(PRF.site) LIKE UPPER (%s) "
        # PS_QUERY = "AND PRF.plan_start >= %s "
        # PE_QUERY = "AND PRF.plan_finish <= %s "
        PC_QUERY = "AND PRF.project_category = %s "
        PT_QUERY = "AND PRF.project_type = %s "
        BU_QUERY = "AND PRF.bu = %s "
        HD_QUERY = "AND PRF.handle_div = %s "
        CL_QUERY = "AND PRF.cancelled = %s "
        CP_QUERY = "AND PRF.complete = %s "
        IB_QUERY = "AND PRF.mis_ib_code = %s "
        EP_QUERY = "AND PRF.mis_ep_code = %s "
        COMMON_ORDER = "ORDER BY PRF.project_year, PRF.project_name, PRF.cancelled ASC"

        with connection.cursor() as cursor:
            if project_year:
                COMMON_QUERY = COMMON_QUERY + PY_QUERY
                sqlParameters.append(project_year)
            if project_name:
                COMMON_QUERY = COMMON_QUERY + PN_QUERY
                sqlParameters.append(project_name + "%")
            if it_pm:
                COMMON_QUERY = COMMON_QUERY + IP_QUERY
                sqlParameters.append("%" + it_pm + "%")
            if site:
                COMMON_QUERY = COMMON_QUERY + SITE_QUERY
                sqlParameters.append("%" + site + "%")
            # if plan_date_star:
            #     COMMON_QUERY = COMMON_QUERY + PS_QUERY
            #     sqlParameters.append(plan_date_star)
            # if plan_date_end:
            #     COMMON_QUERY = COMMON_QUERY + PE_QUERY
            #     sqlParameters.append(plan_date_end)
            if project_cate:
                COMMON_QUERY = COMMON_QUERY + PC_QUERY
                sqlParameters.append(project_cate)
            if project_type:
                COMMON_QUERY = COMMON_QUERY + PT_QUERY
                sqlParameters.append(project_type)
            if bu:
                COMMON_QUERY = COMMON_QUERY + BU_QUERY
                sqlParameters.append(bu)
            if handle_div:
                COMMON_QUERY = COMMON_QUERY + HD_QUERY
                sqlParameters.append(handle_div)
            if cancel:
                COMMON_QUERY = COMMON_QUERY + CL_QUERY
                sqlParameters.append(cancel)
            if complete:
                COMMON_QUERY = COMMON_QUERY + CP_QUERY
                sqlParameters.append(complete)
            if ib_code:
                COMMON_QUERY = COMMON_QUERY + IB_QUERY
                sqlParameters.append(ib_code)
            if ep_code:
                COMMON_QUERY = COMMON_QUERY + EP_QUERY
                sqlParameters.append(ep_code)

            cursor.execute(COMMON_QUERY + COMMON_ORDER, sqlParameters)

            result = namedtuplefetchall(cursor)
            return Response(result)

    @action(detail=False, methods=["post"])
    def query_prf_by_upload(self, request, pk=None):
        sqlParameters = []
        req = request.data
        project_year = req.get("project_year").upper().split(",")
        project_name = req.get("project_name").upper().split(",")

        COMMON_QUERY = """SELECT PRF.id, PRF.project_year, PRF.project_name, PRF.it_pm, PRF.biz_owner, PRF.contact_window, PRF.customer, PRF.site,
PRF.plan_start, PRF.plan_finish, PRF.recv_ep_code, PRF.comments, PRF.cancelled, PRF.complete, PRF.bud_syst_recv_chg_dept, PRF.bu, PRF.bg, PRF.bo, PRF.handle_div, PRF.project_category, PRF.project_type, PRF.recv_chg_dept, PRF.mis_ib_code, PRF.mis_ep_code, PRF.creatdate, PRF.creater, PRF.updatedate, PRF.updater, '' AS prf_ln FROM imp_prf PRF WHERE 1=1 """
        PY_QUERY = "AND PRF.project_year = ANY(%s) "
        PN_QUERY = "AND UPPER(PRF.project_name) = ANY(%s) "
        COMMON_ORDER = "ORDER BY PRF.project_year, PRF.project_name, PRF.cancelled, PRF.complete ASC"

        with connection.cursor() as cursor:
            if project_year:
                COMMON_QUERY = COMMON_QUERY + PY_QUERY
                sqlParameters.append(project_year)

            if project_name:
                COMMON_QUERY = COMMON_QUERY + PN_QUERY
                sqlParameters.append(project_name)

            cursor.execute(COMMON_QUERY + COMMON_ORDER, sqlParameters)

            result = namedtuplefetchall(cursor)
            return Response(result)

    @swagger_auto_schema(
        method='post',
        operation_summary="generate PRF's PDF by PRF's id",
        operation_description="generate PRF's PDF by PRF's id",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "prf_id": openapi.Schema(type=openapi.TYPE_STRING, description="PRF ID"),
                "project_year": openapi.Schema(type=openapi.TYPE_STRING, description="PRF Project Year"),
                "project_name": openapi.Schema(type=openapi.TYPE_STRING, description="PRF Project Name"),
                "mis_ep_code": openapi.Schema(type=openapi.TYPE_STRING, description="PRF MIS EP Code"),
                "mis_ib_code": openapi.Schema(type=openapi.TYPE_STRING, description="PRF MIS IB Code")
            }
        ),
    )
    @action(detail=False, methods=["post"])
    def generate_PRF_PDF(self, request, pk=None):
        data = {"code": 0,"msg": "","data": []}
        try:
            req = request.data
            prf_id = req.get("prf_id")
            project_year = req.get("project_year")
            project_name = req.get("project_name")
            ep_code = req.get("mis_ep_code")
            ib_code = req.get("mis_ib_code")
            prf = getPRFData(prf_id, project_year, project_name, ep_code, ib_code)
            if len(prf):
                prfln = getPRFLNData(prf_id, project_year, project_name)
                if len(prfln):
                    # data["code"] = 1
                    # data["msg"] = "Generate PRF's PDF document success"
                    # # data["data"] = generatePRFPDFDocument(prf, prfln)
                    return generatePRFPDFDocument(prf, prfln)
                else:
                    data["code"] = 1
                    data["msg"] = "No PRF data, Project Name:" + project_name + "IB Code:" + ib_code
                    return JsonResponse(data)
            else:
                data["code"] = 1
                data["msg"] = "No PRF data, Project Name:" + project_name + "IB Code:" + ib_code
                return JsonResponse(data)
        except Exception as e:
            data["code"] = 1
            data["msg"] = "Generate PRF by PDF fail! error message:" + e
            return JsonResponse(data)

    @action(detail=False,methods=["post"])
    def download_file(self,request,pk=None):
        data = {"code": 0 ,"msg":" ", "data": []}
        pajTxt_columns = ["ISSUE DEPT","ISSUE PCODE","*CURRENCY",
                        "Add Reviewer1","Add Reviewer2","Charge Type",
                        "Short Remark","*Remark","Receive Dept",
                        "Receive PCode","*Amount","*Item Text",
                        "Assignment","Business Type","*Customer name",
                        "*Reason","SBG Charge Type","Applicant"]
        jan_columns = ["Handle Div","BO","BG",
                      "BU","PRF Project Name","PMCS IB Proj Name",
                      "MIS IB Code","IT PM","Biz Owner",
                      "Contact Window","Recv Charge Dept","Recv EP Code",
                      "ResourceDiv.","Jan-Budget","Jan-Plan",
                      "Jan-TSS","Jan-PAJ","Proj Catgegory",
                      "Proj Type","PAJ Charge"]
        # 有關時間column 的處理
        jan_columns[13] = getHeadColumnsPlan() + "-Budget"
        jan_columns[14] = getHeadColumnsPlan() + "-Plan"
        jan_columns[15] = getHeadColumnsPlan() + "-TSS"
        jan_columns[16] = getHeadColumnsPlan() + "-PAJ"
        chargePaj_columns = ["Project HC Support","Charge From","Charge To","Jan-PAJ-MM","Amount"]
        # 有關時間column 的處理
        chargePaj_columns[3] = getHeadColumnsPlan() + "-PAJ-MM"
        #拼接table2的數據
        prf_data_list = getPrf()
        excel_data = []
        for prf_data in prf_data_list:
            print(".....................",prf_data)
            project_name = prf_data.get("project_name")
            project_year = prf_data.get("project_year")
            mis_ib_code = prf_data.get("mis_ib_code")
            #TODO project_name不存在問題
            handle_div_data = getHandleDiv(mis_ib_code,project_year,project_name)
            handle_div = handle_div_data.get("div_group")
            month_time = getMonthPlan()
            #O columns
            month_plan = handle_div_data.get(month_time)
            #TODO 一對多的問題
            resource_div_data = getRsourceDiv(project_year,project_name)
            resource_div = resource_div_data.get("div_group")
            # N columns
            month_Budget = resource_div_data.get(month_time)
            jan_tss = getJanTss(mis_ib_code,project_year,project_name).get("tss_mm")
            jan_paj = getMonthPlanFromIbln(project_year,project_name)
            paj_charge = getPajCharge(handle_div,resource_div,jan_paj)
            # table2每一行的數據
            row_data = [handle_div,prf_data.get("bo"),prf_data.get("bg"),
                        prf_data.get("bu"),project_name,prf_data.get("pmcs_ib_project_name"),
                        mis_ib_code,prf_data.get("it_pm"),prf_data.get("biz_owner"),
                        prf_data.get("contact_window"),prf_data.get("recv_chg_dept"),prf_data.get("recv_ep_code"),
                        resource_div,month_Budget,month_plan,
                        jan_tss,jan_paj,prf_data.get("project_category"),
                        prf_data.get("project_type"),paj_charge]

            excel_data.append(row_data)
        df = pd.DataFrame(excel_data,index=None,columns=jan_columns)
        #table3 的數據
        df_data = df[["Handle Div","ResourceDiv.","PRF Project Name",jan_columns[16]]].sort_values(by=jan_columns[16],ascending=False)
        # df_cal_data 是有效的計算資料
        df_cal_data = df_data[df["Handle Div"] != df["ResourceDiv."]].copy(deep=True)
        df_cal_data = df_data[df[jan_columns[16]] > 0.1]
        # 根據project_name查找
        df_project_had = df_cal_data[["PRF Project Name","Handle Div"]].drop_duplicates().reset_index().drop(columns="index").copy(deep=True)
        arr_project = []
        for row in df_project_had.iterrows():
            project_name = row[1]["PRF Project Name"]
            _had_div = row[1]["Handle Div"]
            print("="*80)
            #過濾自己部門的project_name
            df__ = df_cal_data.where(
                                     (df_cal_data["PRF Project Name"] == project_name)&
                                     (df_cal_data["ResourceDiv."] != _had_div)&
                                     (df_cal_data[jan_columns[16]] > 0 )
                                     ).copy(deep=True).dropna().sort_values(by=jan_columns[16])
            df_test = df__.copy(deep=True)
            for idx,row_sub in df_test.iterrows():
                _res_div = row_sub["ResourceDiv."]
                # print("要給我錢的 ",_res_div,'->',_had_div)
                df_test2 = df_cal_data.where(
                                             (df_cal_data["Handle Div"] == _res_div) &
                                             (df_cal_data["ResourceDiv."] == _had_div) &
                                             (df_cal_data[jan_columns[16]] > 0)
                                            ).copy(deep=True).dropna().sort_values(by=jan_columns[16])
                for index,row_cal in df_test2.iterrows():
                    if df_test.loc[idx,jan_columns[16]] == 0:
                        continue
                    _mm_sub = row_cal[jan_columns[16]]
                    if _mm_sub == df_test.loc[idx,jan_columns[16]] and df_test.loc[idx,jan_columns[16]] > 0:
                        df_cal_data.loc[index,jan_columns[16]] = 0
                        df_test[idx,jan_columns[16]] = 0
                        _mm_sub = 0
                    elif _mm_sub > df_test.loc[idx,jan_columns[16]] and df_test.loc[idx,jan_columns[16]] > 0:
                        df_cal_data.loc[index,jan_columns[16]] = df_cal_data.loc[index,jan_columns[16]] - df_test.loc[idx,jan_columns[16]]
                        df_test.loc[idx,jan_columns[16]] = 0
                    elif _mm_sub < df_test.loc[idx,jan_columns[16]] and df_test.loc[idx,jan_columns[16]] > 0:
                        df_test.loc[idx,jan_columns[16]] = df_test.loc[idx,jan_columns[16]] - row_cal[jan_columns[16]]
                        df_cal_data.loc[index,jan_columns[16]] = 0
            arr_project.append(df_test)
        df_project_all = pd.concat(arr_project).sort_values(by=["Handle Div","ResourceDiv."],ascending=[True, True])
        # table3的最終結果
        df_charge_paj_data = handleChargePajData(df_project_all,chargePaj_columns)
        print("...........df_charge_paj_data...............",df_charge_paj_data)
        # table1數據處理
        df_charge_paj_data_list = df_charge_paj_data.values.tolist()
        df_project_all_list = df_project_all.values.tolist()
        project_year = datetime.datetime.now().year
        q_pajUp = []
        for df_data in df_project_all_list:
            hindle_div_ = df_data[0]
            resources_div_ = df_data[1]
            project_name = df_data[2]
            issue_dept = get_dept_by_div(hindle_div_)
            receive_dept = get_dept_by_div(resources_div_)
            amount = ""
            item_txt = ""
            for df_charge_paj in df_charge_paj_data_list:
                if df_charge_paj[1] == hindle_div_ and df_charge_paj[2] == resources_div_:
                    amount = df_charge_paj[4]
                    item_txt = hindle_div_ + "HC*" + str(df_charge_paj[3])
                    break
            remark = str(project_year) + "/" + getHeadColumnsPlan() + "-BU/Function Project HC Internal Charge from" + hindle_div_ + "to" + resources_div_
            print("............remark..........",remark)
            impPrf = get_data_from_prf(project_year,project_name)
            table1_data = [issue_dept,"","","","","","",remark,receive_dept,impPrf.get("recv_ep_code"),
                           amount,item_txt,"","",impPrf.get("cqustomer"),"","",impPrf.get("it_pm")]
            q_pajUp.append(table1_data)
        df_table1= pd.DataFrame(q_pajUp,index=None,columns=pajTxt_columns)
        # 寫入到IO
        output = BytesIO()
        file_name = "PAJ-ML0000.xlsx"
        writer = pd.ExcelWriter(output)
        with writer:
            df_table1.to_excel(writer,sheet_name="Q_PAJUploadFile3",encoding="utf-8",index=False) # table1
            df.to_excel(writer,sheet_name="Jan-BUFunction Project HC Data",encoding="utf-8",index=False) #table2
            df_charge_paj_data.to_excel(writer,sheet_name="Internal Charge -PAJ",encoding="uf-8",index=False) #table3
        #重新定位到開始
        output.seek(0)
        writer.save()
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response.write(codecs.BOM_UTF8)
        response.content = output.getvalue()
        file_name = urlquote(file_name)
        response['Content-Disposition'] = 'attachment;filename=%s' % file_name
        return response

def get_dept_by_div(divsion):
    dept_value = ImpDiv.objects.filter(div_group = divsion).values("div").first().get("div")
    return dept_value

def get_data_from_prf(project_year,project_name):
    impPrf = ImpPrf.objects.filter(project_year=project_year,project_name=project_name).values().first()
    return impPrf

def handleChargePajData(df_project_all,chargePaj_columns):
    charge_paj_data = {}
    for item in df_project_all.values.tolist():
        key = item[0] + "-" + item[1]
        if key in charge_paj_data.keys():
            charge_paj_data[key] += item[3]
        else:
            charge_paj_data[key] = item[3]
    charge_paj_result = []
    for key in charge_paj_data.keys():
        data = str(key).split("-")
        data.append(charge_paj_data.get(key))
        # Amount = Jan-PAJ-MM * 100000
        data.append(charge_paj_data.get(key) * 100000)
        # 首列插入説明
        data.insert(0,"Internal Charge -PAJ")
        charge_paj_result.append(data)
    df_charge_paj_data = pd.DataFrame(charge_paj_result,index=None,columns=chargePaj_columns)
    return df_charge_paj_data


def getPajCharge(handle_div,resource_div,jan_paj):
    if handle_div == resource_div or int(jan_paj) <= 0.1:
        return "NO"
    else:
        return "YES"

def getMonthPlanFromIbln(project_year,project_name):
    last_month = getMonthPlan()
    month_plan = ImpIbln.objects.filter(project_year=project_year,project_name=project_name).values(last_month).first().get(last_month)
    return month_plan

def getJanTss(mis_ib_code,project_year,project_name):
    #卡時間,當前時間的上一個月
    today = datetime.date.today()
    first = today.replace(day=1)
    last_month_time = first - datetime.timedelta(days=1)
    last_month = str(last_month_time)[5:7]
    jan_tss = ImpTssPast.objects.filter(Q(pmcs_ib_project_year=project_year),
                                        Q(ib_code=mis_ib_code)|
                                        Q(pmcs_ib_project_name=project_name)|
                                        Q(work_month=last_month)).values("tss_mm").first()
    return jan_tss

def getRsourceDiv(project_year,project_name):
    """imp_prfln,resourceDiv"""
    month_plan = getMonthPlan()
    resource_div_l = ImpPrfln.objects.filter(Q(project_year=project_year)|Q(project_name=project_name)).values("div_group",month_plan).first()
    return resource_div_l

def getHandleDiv(ib_code,project_year,project_name):
    """handle_div,Jan-PAJ"""
    month_plan = getMonthPlan()
    handle_div_l = Pajln.objects.filter(Q(ib_code=ib_code)|
                                        Q(project_name=project_name)|
                                        Q(project_year=project_year)).values("div_group",month_plan).first()
    return handle_div_l

def getMonthPlan():
    date_dict = {"01":"jan_plan","02":"feb_plan","03":"mar_plan","04":"apr_plan",
                 "05":"may_plan","06":"jun_plan","07":"jul_plan","08":"aug_plan",
                 "09":"sep_plan","10":"oct_plan","11":"nov_plan","12":"dec_plan"}
    today = datetime.date.today()
    first = today.replace(day=1)
    last_month_time = first - datetime.timedelta(days=1)
    last_month = str(last_month_time)[5:7]
    return date_dict.get(last_month)

# table2 & table3 有關月份的column處理
def getHeadColumnsPlan():
    date_dict = {"01":"Jan","02":"Feb","03":"Mar","04":"Apr",
                 "05":"May","06":"Jun","07":"Jul","08":"Aug",
                 "09":"Sep","10":"Oct","11":"Nov","12":"Dec"}
    today = datetime.date.today()
    first = today.replace(day=1)
    last_month_time = first - datetime.timedelta(days=1)
    last_month = str(last_month_time)[5:7]
    return date_dict.get(last_month)


def getPrf():
    prf_data = ImpPrf.objects.all().values()
    return prf_data

def generatePRFPDFDocument(p_prf, p_prfln):
    pdf = FPDF()
    pdf.add_font("fireflysung","","fireflysung.ttf",uni=True)
    pdf.add_page(orientation="L")
    pdf.set_font("fireflysung", size=10)
    line_height = pdf.font_size * 2.5
    col_width = pdf.fw /4
    #Generate PDF"s Header for image
    pdf.image("wistron_logo.JPG",9.1,0,282,20)
    pdf.ln()
    pdf.cell(240, 8, "",border=0)
    pdf.ln()
    pdf.cell(40, 8, "Dept:" + p_prf[0]["handle_div"],border=0)
    pdf.cell(200, 8, "",border=0)
    pdf.cell(40, 8, "Issued Date:"+ datetime.datetime.now().strftime("%Y-%m-%d"),border=0)
    pdf.ln()
    pdf.cell(40, 8, "Project Name:",border=1)
    pdf.cell(240, 8, p_prf[0]["project_name"],border=1)
    pdf.ln()
    pdf.cell(40, 8, "Biz Owner:",border=1)
    pdf.cell(100, 8, p_prf[0]["biz_owner"],border=1)
    pdf.cell(40, 8, "Contact Window:",border=1)
    pdf.cell(100, 8, p_prf[0]["contact_window"],border=1)
    pdf.ln()
    pdf.cell(40, 8, "Customer:",border=1)
    pdf.cell(50, 8, p_prf[0]["customer"],border=1)
    pdf.cell(40, 8, "End Customer:",border=1)
    pdf.cell(50, 8, p_prf[0]["end_customer"],border=1)
    pdf.cell(40, 8, "Sites:",border=1)
    pdf.cell(60, 8, p_prf[0]["site"],border=1)
    pdf.ln()
    pdf.cell(40, 8, "Billing Type:",border=1)
    pdf.cell(50, 8, p_prf[0]["Billing_Type"],border=1)
    pdf.cell(40, 8, "Receiver Project Code:",border=1)
    pdf.cell(50, 8, p_prf[0]["Receiver_Project_Code"],border=1)
    pdf.cell(40, 8, "Receiver Charge Dept:",border=1)
    pdf.cell(60, 8, p_prf[0]["Receiver_Charge_Dept"],border=1)
    pdf.ln()
    pdf.cell(40, 8, "Project Type:",border=1)
    pdf.cell(50, 8, p_prf[0]["Project_Type"],border=1)
    pdf.cell(40, 8, "IT PM:",border=1)
    pdf.cell(50, 8, p_prf[0]["it_pm"],border=1)
    pdf.cell(40, 8, "Charge Amount(NT):",border=1)
    pdf.cell(60, 8, str(p_prf[0]["Charge_Amount"]),border=1)
    pdf.ln()
    pdf.cell(40, 8, "Draft Schedule:",border=1)
    pdf.cell(100, 8, p_prf[0]["plan_start"].strftime("%Y/%m/%d") + "~" + p_prf[0]["plan_finish"].strftime("%Y/%m/%d"),border=1)
    pdf.cell(40, 8, "Project Duration:",border=1)
    pdf.cell(100, 8, str(p_prf[0]["Project_Duration"])+"Month(s)",border=1)
    pdf.ln()
    pdf.ln()
    #Generate Man power
    pdf.cell(40, 8, "Manpower:",border=1)
    pdf.cell(30, 8, "ML10",border=1,align="C")
    pdf.cell(30, 8, "ML20",border=1,align="C")
    pdf.cell(30, 8, "ML60",border=1,align="C")
    pdf.cell(30, 8, "ML70",border=1,align="C")
    pdf.cell(30, 8, "ML80",border=1,align="C")
    pdf.cell(30, 8, "MLD0",border=1,align="C")
    pdf.cell(30, 8, "MLL0",border=1,align="C")
    pdf.cell(30, 8, "Total Manpower",border=1,align="C")
    pdf.ln()
    pdf.cell(40, 8, "Man-Month:",border=1)
    pdf.cell(30, 8, str(p_prf[0]["ML10_Man_Power"]),border=1,align="C")
    pdf.cell(30, 8, str(p_prf[0]["ML20_Man_Power"]),border=1,align="C")
    pdf.cell(30, 8, str(p_prf[0]["ML60_Man_Power"]),border=1,align="C")
    pdf.cell(30, 8, str(p_prf[0]["ML70_Man_Power"]),border=1,align="C")
    pdf.cell(30, 8, str(p_prf[0]["ML80_Man_Power"]),border=1,align="C")
    pdf.cell(30, 8, str(p_prf[0]["MLD0_Man_Power"]),border=1,align="C")
    pdf.cell(30, 8, str(p_prf[0]["MLL0_Man_Power"]),border=1,align="C")
    pdf.cell(30, 8, str(p_prf[0]["Total_Manpower"]),border=1,align="C")
    pdf.ln()
    pdf.cell(40, 30, "Project Description:",border=1)
    pdf.cell(240, 30, p_prf[0]["comments"],border=1)
    pdf.ln()
    pdf.cell(40, 8, "Attachment(s):",border=1)
    pdf.cell(240, 8, "",border=1)
    pdf.ln()
    pdf.cell(40, 8, 'Div',border=1,align="C")
    pdf.cell(20, 8, 'Jan',border=1,align="C")
    pdf.cell(20, 8, 'Feb',border=1,align="C")
    pdf.cell(20, 8, 'Mar',border=1,align="C")
    pdf.cell(20, 8, 'Apr',border=1,align="C")
    pdf.cell(20, 8, 'May',border=1,align="C")
    pdf.cell(20, 8, 'Jun',border=1,align="C")
    pdf.cell(20, 8, 'Jul',border=1,align="C")
    pdf.cell(20, 8, 'Aug',border=1,align="C")
    pdf.cell(20, 8, 'Sep',border=1,align="C")
    pdf.cell(20, 8, 'Oct',border=1,align="C")
    pdf.cell(20, 8, 'Nov',border=1,align="C")
    pdf.cell(20, 8, 'Dec',border=1,align="C")
    pdf.ln()
    #Generate PRF Detail
    for item in p_prfln:
        pdf.cell(40, 8, str(item["div_group"]),border=1,align="C")
        pdf.cell(20, 8, str(item["jan_plan"]),border=1,align="C")
        pdf.cell(20, 8, str(item["feb_plan"]),border=1,align="C")
        pdf.cell(20, 8, str(item["mar_plan"]),border=1,align="C")
        pdf.cell(20, 8, str(item["apr_plan"]),border=1,align="C")
        pdf.cell(20, 8, str(item["may_plan"]),border=1,align="C")
        pdf.cell(20, 8, str(item["jun_plan"]),border=1,align="C")
        pdf.cell(20, 8, str(item["jul_plan"]),border=1,align="C")
        pdf.cell(20, 8, str(item["aug_plan"]),border=1,align="C")
        pdf.cell(20, 8, str(item["sep_plan"]),border=1,align="C")
        pdf.cell(20, 8, str(item["oct_plan"]),border=1,align="C")
        pdf.cell(20, 8, str(item["nov_plan"]),border=1,align="C")
        pdf.cell(20, 8, str(item["dec_plan"]),border=1,align="C")
        pdf.ln()
    # Generate PDF document in load
    pdf.output((''.join(filter(str.isalnum, str(p_prf[0]["project_name"])))) + '.pdf')
    # Generate HttpResponse for front_end download PDF
    fs = FileSystemStorage()
    filename = (''.join(filter(str.isalnum, str(p_prf[0]["project_name"])))) + '.pdf'
    if fs.exists(filename):
        with fs.open(filename) as openPdf:
            response = HttpResponse(openPdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
            return response
    else:
        return HttpResponseNotFound('The requested pdf was not found in our server.')

def getPRFLNData(prf_id, project_year, project_name):
    sqlParameters = []
    COMMON_QUERY = """SELECT PRFLN.div_group, PRFLN.jan_plan, PRFLN.feb_plan, PRFLN.mar_plan, PRFLN.apr_plan, PRFLN.may_plan, PRFLN.jun_plan, PRFLN.jul_plan, PRFLN.aug_plan, PRFLN.sep_plan, PRFLN.oct_plan, PRFLN.nov_plan, PRFLN.dec_plan
FROM imp_prfln PRFLN WHERE 1=1 """
    PY_QUERY = "AND PRFLN.project_year = %s "
    PN_QUERY = "AND PRFLN.project_name = %s "
    PI_QUERY = "AND PRFLN.prf_id = %s "
    COMMON_ORDER = "ORDER BY PRFLN.div_group ASC"
    with connection.cursor() as cursor:
        if project_year:
            COMMON_QUERY = COMMON_QUERY + PI_QUERY
            sqlParameters.append(prf_id)
        if project_year:
            COMMON_QUERY = COMMON_QUERY + PY_QUERY
            sqlParameters.append(project_year)
        if project_name:
            COMMON_QUERY = COMMON_QUERY + PN_QUERY
            sqlParameters.append(project_name)
        cursor.execute(COMMON_QUERY + COMMON_ORDER, sqlParameters)
        result = namedtuplefetchall_prfln(cursor)
        return result

def getPRFData(prf_id, project_year, project_name, ep_code, ib_code):
    sqlParameters = []
    COMMON_QUERY = """SELECT PRF.handle_div, PRF.project_name, PRF.biz_owner, PRF.contact_window, (PRF.bg || '/' || PRF.bu) AS customer, PRF.customer AS end_customer, PRF.site,
 'Charged' AS Billing_Type, PRF.recv_ep_code AS Receiver_Project_Code, PRF.recv_chg_dept AS Receiver_Charge_Dept, 'Development' AS Project_Type, PRF.it_pm,
 (COALESCE(AMT.Man_Month, 0) * COALESCE(AMT.rate, 0)) AS Charge_Amount, PRF.plan_start, PRF.plan_finish,
 ((DATE_PART('year', PRF.plan_finish::date) - DATE_PART('year', PRF.plan_start::date)) * 12 + (DATE_PART('month', PRF.plan_finish::date) - DATE_PART('month', PRF.plan_start::DATE))) AS Project_Duration,
 COALESCE(ML10.Man_Power, 0) AS ML10_Man_Power, COALESCE(ML20.Man_Power, 0) AS ML20_Man_Power, COALESCE(ML60.Man_Power, 0) AS ML60_Man_Power, COALESCE(ML70.Man_Power, 0) AS ML70_Man_Power,
 COALESCE(ML80.Man_Power, 0) AS ML80_Man_Power, COALESCE(MLD0.Man_Power, 0) AS MLD0_Man_Power, COALESCE(MLL0.Man_Power, 0) AS MLL0_Man_Power, COALESCE(AMT.Man_Month, 0) AS Total_Manpower,
 PRF.comments
 FROM imp_prf PRF
 LEFT JOIN (SELECT PRFLN.project_year, PRFLN.project_name, PRFLN.prf_id, SUM(PRFLN.jan_plan + PRFLN.feb_plan + PRFLN.mar_plan + PRFLN.apr_plan + PRFLN.may_plan + PRFLN.jun_plan + PRFLN.jul_plan + PRFLN.aug_plan + PRFLN.sep_plan + PRFLN.oct_plan + PRFLN.nov_plan + PRFLN.dec_plan) AS Man_Month
, DIV.rate FROM imp_prfln PRFLN LEFT JOIN imp_div DIV ON PRFLN.div_group = DIV.div_group GROUP BY PRFLN.project_year, PRFLN.project_name, PRFLN.prf_id, DIV.rate) AMT
	ON PRF.id = AMT.prf_id AND PRF.project_year = AMT.project_year AND PRF.project_name = AMT.project_name
 LEFT JOIN (SELECT project_year, project_name, div_group, prf_id, SUM(jan_plan + feb_plan + mar_plan + apr_plan + may_plan + jun_plan + jul_plan + aug_plan + sep_plan + oct_plan + nov_plan + dec_plan) AS Man_Power FROM imp_prfln WHERE div_group = 'ML10' GROUP BY project_year, project_name, div_group, prf_id) ML10
 	ON PRF.id = ML10.prf_id AND PRF.project_year = ML10.project_year AND PRF.project_name = ML10.project_name
 LEFT JOIN (SELECT project_year, project_name, div_group, prf_id, SUM(jan_plan + feb_plan + mar_plan + apr_plan + may_plan + jun_plan + jul_plan + aug_plan + sep_plan + oct_plan + nov_plan + dec_plan) AS Man_Power FROM imp_prfln WHERE div_group = 'ML20' GROUP BY project_year, project_name, div_group, prf_id) ML20
	ON PRF.id = ML20.prf_id AND PRF.project_year = ML20.project_year AND PRF.project_name = ML20.project_name
 LEFT JOIN (SELECT project_year, project_name, div_group, prf_id, SUM(jan_plan + feb_plan + mar_plan + apr_plan + may_plan + jun_plan + jul_plan + aug_plan + sep_plan + oct_plan + nov_plan + dec_plan) AS Man_Power FROM imp_prfln WHERE div_group = 'ML60' GROUP BY project_year, project_name, div_group, prf_id) ML60
 	ON PRF.id = ML60.prf_id AND PRF.project_year = ML60.project_year AND PRF.project_name = ML60.project_name
 LEFT JOIN (SELECT project_year, project_name, div_group, prf_id, SUM(jan_plan + feb_plan + mar_plan + apr_plan + may_plan + jun_plan + jul_plan + aug_plan + sep_plan + oct_plan + nov_plan + dec_plan) AS Man_Power FROM imp_prfln WHERE div_group = 'ML70' GROUP BY project_year, project_name, div_group, prf_id) ML70
	ON PRF.id = ML70.prf_id AND PRF.project_year = ML70.project_year AND PRF.project_name = ML70.project_name
 LEFT JOIN (SELECT project_year, project_name, div_group, prf_id, SUM(jan_plan + feb_plan + mar_plan + apr_plan + may_plan + jun_plan + jul_plan + aug_plan + sep_plan + oct_plan + nov_plan + dec_plan) AS Man_Power FROM imp_prfln WHERE div_group = 'ML80' GROUP BY project_year, project_name, div_group, prf_id) ML80
	ON PRF.id = ML80.prf_id AND PRF.project_year = ML80.project_year AND PRF.project_name = ML80.project_name
 LEFT JOIN (SELECT project_year, project_name, div_group, prf_id, SUM(jan_plan + feb_plan + mar_plan + apr_plan + may_plan + jun_plan + jul_plan + aug_plan + sep_plan + oct_plan + nov_plan + dec_plan) AS Man_Power FROM imp_prfln WHERE div_group = 'MLD0' GROUP BY project_year, project_name, div_group, prf_id) MLD0
	ON PRF.id = MLD0.prf_id AND PRF.project_year = MLD0.project_year AND PRF.project_name = MLD0.project_name
 LEFT JOIN (SELECT project_year, project_name, div_group, prf_id, SUM(jan_plan + feb_plan + mar_plan + apr_plan + may_plan + jun_plan + jul_plan + aug_plan + sep_plan + oct_plan + nov_plan + dec_plan) AS Man_Power FROM imp_prfln WHERE div_group = 'MLL0' GROUP BY project_year, project_name, div_group, prf_id) MLL0
	ON PRF.id = MLL0.prf_id AND PRF.project_year = MLL0.project_year AND PRF.project_name = MLL0.project_name
 WHERE 1=1 """
    ID_QUERY = "AND PRF.id = %s "
    PY_QUERY = "AND PRF.project_year = %s "
    PN_QUERY = "AND PRF.project_name = %s "
    EP_QUERY = "AND PRF.mis_ep_code = %s "
    IB_QUERY = "AND PRF.mis_ib_code = %s "
    COMMON_ORDER = "ORDER BY PRF.id, PRF.project_year, PRF.project_name ASC"
    with connection.cursor() as cursor:
        if prf_id:
            COMMON_QUERY = COMMON_QUERY + ID_QUERY
            sqlParameters.append(prf_id)
        if project_year:
            COMMON_QUERY = COMMON_QUERY + PY_QUERY
            sqlParameters.append(project_year)
        if project_name:
            COMMON_QUERY = COMMON_QUERY + PN_QUERY
            sqlParameters.append(project_name)
        if ib_code:
            COMMON_QUERY = COMMON_QUERY + IB_QUERY
            sqlParameters.append(ib_code)
        if ep_code:
            COMMON_QUERY = COMMON_QUERY + EP_QUERY
            sqlParameters.append(ep_code)
        cursor.execute(COMMON_QUERY + COMMON_ORDER, sqlParameters)
        result = namedtuplefetchall_prf(cursor)
    return result

def namedtuplefetchall_prfln(cursor):
    # Return all rows from a cursor as a namedtuple
    # desc = cursor.description
    nt_result = namedtuple(
        "Result",
        [
            "div_group",
            "jan_plan",
            "feb_plan",
            "mar_plan",
            "apr_plan",
            "may_plan",
            "jun_plan",
            "jul_plan",
            "aug_plan",
            "sep_plan",
            "oct_plan",
            "nov_plan",
            "dec_plan",

        ],
    )
    result = [nt_result(*row) for row in cursor.fetchall()]
    result = [
        {
            "div_group": r.div_group,
            "jan_plan": r.jan_plan,
            "feb_plan": r.feb_plan,
            "mar_plan": r.mar_plan,
            "apr_plan": r.apr_plan,
            "may_plan": r.may_plan,
            "jun_plan": r.jun_plan,
            "jul_plan": r.jul_plan,
            "aug_plan": r.aug_plan,
            "sep_plan": r.sep_plan,
            "oct_plan": r.oct_plan,
            "nov_plan": r.nov_plan,
            "dec_plan": r.dec_plan
        }
        for r in result
    ]
    return result

def namedtuplefetchall_prf(cursor):
    # Return all rows from a cursor as a namedtuple
    # desc = cursor.description
    nt_result = namedtuple(
        "Result",
        [
            "handle_div",
            "project_name",
            "biz_owner",
            "contact_window",
            "customer",
            "end_customer",
            "site",
            "Billing_Type",
            "Receiver_Project_Code",
            "Receiver_Charge_Dept",
            "Project_Type",
            "it_pm",
            "Charge_Amount",
            "plan_start",
            "plan_finish",
            "Project_Duration",
            "ML10_Man_Power",
            "ML20_Man_Power",
            "ML60_Man_Power",
            "ML70_Man_Power",
            "ML80_Man_Power",
            "MLD0_Man_Power",
            "MLL0_Man_Power",
            "Total_Manpower",
            "comments"
        ],
    )
    result = [nt_result(*row) for row in cursor.fetchall()]
    result = [
        {
            "handle_div": r.handle_div,
            "project_name": r.project_name,
            "biz_owner": r.biz_owner,
            "contact_window": r.contact_window,
            "customer": r.customer,
            "end_customer": r.end_customer,
            "site": r.site,
            "Billing_Type": r.Billing_Type,
            "Receiver_Project_Code": r.Receiver_Project_Code,
            "Receiver_Charge_Dept": r.Receiver_Charge_Dept,
            "Project_Type": r.Project_Type,
            "it_pm": r.it_pm,
            "Charge_Amount": r.Charge_Amount,
            "plan_start": r.plan_start,
            "plan_finish": r.plan_finish,
            "Project_Duration": r.Project_Duration,
            "ML10_Man_Power": r.ML10_Man_Power,
            "ML20_Man_Power": r.ML20_Man_Power,
            "ML60_Man_Power": r.ML60_Man_Power,
            "ML70_Man_Power": r.ML70_Man_Power,
            "ML80_Man_Power": r.ML80_Man_Power,
            "MLD0_Man_Power": r.MLD0_Man_Power,
            "MLL0_Man_Power": r.MLL0_Man_Power,
            "Total_Manpower": r.Total_Manpower,
            "comments": r.comments
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
            "project_year",
            "project_name",
            "it_pm",
            "biz_owner",
            "contact_window",
            "customer",
            "site",
            "plan_start",
            "plan_finish",
            "recv_ep_code",
            "comments",
            "cancelled",
            "complete",
            "bud_syst_recv_chg_dept",
            "bu",
            "bg",
            "bo",
            "handle_div",
            "project_category",
            "project_type",
            "recv_chg_dept",
            "mis_ib_code",
            "mis_ep_code",
            "creatdate",
            "creater",
            "updatedate",
            "updater",
            "prf_ln",
        ],
    )
    result = [nt_result(*row) for row in cursor.fetchall()]
    result = [
        {
            "id": r.id,
            "project_year": r.project_year,
            "project_name": r.project_name,
            "it_pm": r.it_pm,
            "biz_owner": r.biz_owner,
            "contact_window": r.contact_window,
            "customer": r.customer,
            "site": r.site,
            "plan_start": r.plan_start,
            "plan_finish": r.plan_finish,
            "recv_ep_code": r.recv_ep_code,
            "comments": r.comments,
            "cancelled": r.cancelled,
            "complete": r.complete,
            "bud_syst_recv_chg_dept": r.bud_syst_recv_chg_dept,
            "bu": r.bu,
            "bg": r.bg,
            "bo": r.bo,
            "div": r.handle_div,
            "project_category": r.project_category,
            "project_type": r.project_type,
            "recv_chg_dept": r.recv_chg_dept,
            "mis_ib_code": r.mis_ib_code,
            "mis_ep_code": r.mis_ep_code,
            "creatdate": r.creatdate,
            "creater": r.creater,
            "updatedate": r.updatedate,
            "updater": r.updater,
            "prf_ln": getPRFln(r.id, r.project_year, r.project_name),
        }
        for r in result
    ]
    return result

def getPRFln(prf_id, project_year, project_name):
    COMMON_QUERY = """SELECT PRFLN.id, PRFLN.prf_id, PRFLN.jan_plan, PRFLN.feb_plan, PRFLN.mar_plan, PRFLN.apr_plan, PRFLN.may_plan,
PRFLN.jun_plan, PRFLN.jul_plan, PRFLN.aug_plan, PRFLN.sep_plan, PRFLN.oct_plan, PRFLN.nov_plan, PRFLN.dec_plan,
PRFLN.div_group, PRFLN.creatdate, PRFLN.creater, PRFLN.updatedate, PRFLN.updater, div."div", div."functions"
FROM imp_prfln PRFLN LEFT JOIN imp_div div ON PRFLN.div_group = div.div_group WHERE PRFLN.prf_id = %s AND PRFLN.project_year = %s AND PRFLN.project_name = %s """
    COMMON_ORDER = "ORDER BY PRFLN.prf_id, PRFLN.div_group ASC"
    with connection.cursor() as cursor:
        cursor.execute(
            COMMON_QUERY + COMMON_ORDER, [prf_id, project_year, project_name]
        )
        result = namedtuplefetchallPlan(cursor)
        return result

def namedtuplefetchallPlan(cursor):
    # Return all rows from a cursor as a namedtuple
    # desc = cursor.description
    nt_result = namedtuple(
        "Result",
        [
            "id",
            "prf_id",
            "jan_plan",
            "feb_plan",
            "mar_plan",
            "apr_plan",
            "may_plan",
            "jun_plan",
            "jul_plan",
            "aug_plan",
            "sep_plan",
            "oct_plan",
            "nov_plan",
            "dec_plan",
            "div_group",
            "creatdate",
            "creater",
            "updatedate",
            "updater",
            "div",
            "functions",
        ],
    )
    result = [nt_result(*row) for row in cursor.fetchall()]
    result = [
        {
            "id": r.id,
            "prf_id": r.prf_id,
            "jan_plan": r.jan_plan,
            "feb_plan": r.feb_plan,
            "mar_plan": r.mar_plan,
            "apr_plan": r.apr_plan,
            "may_plan": r.may_plan,
            "jun_plan": r.jun_plan,
            "jul_plan": r.jul_plan,
            "aug_plan": r.aug_plan,
            "sep_plan": r.sep_plan,
            "oct_plan": r.oct_plan,
            "nov_plan": r.nov_plan,
            "dec_plan": r.dec_plan,
            "div_group": r.div_group,
            "creatdate": r.creatdate,
            "creater": r.creater,
            "updatedate": r.updatedate,
            "updater": r.updater,
            "div": r.div,
            "functions": r.functions,
        }
        for r in result
    ]
    return result
