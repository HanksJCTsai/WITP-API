# from asyncio.windows_events import NULL
from argparse import Action
from collections import namedtuple
import calendar
from datetime import date, datetime
import string
import traceback

from django.contrib.auth.models import Group, User
from django.db import connection

from django.db.models.query_utils import Q
from django.http.response import HttpResponse, JsonResponse
from imp_bu.models import ImpBu
from imp_bud.models import ImpBud
from imp_budln.models import ImpBudln
from imp_prf.models import ImpPrf
from imp_prfln.models import ImpPrfln
from imp_ib.models import ImpIb
from imp_ibln.models import ImpIbln
from imp_div.models import ImpDiv
from imp_projcategory.models import ProjCategory
from imp_projtype.models import ProjType
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework import permissions, viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from collections import namedtuple


def get_permissions(self):
    # 決定哪些method需要哪些認證
    # GET不用
    if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
        return [permissions.IsAuthenticated()]
    else:
        return [permissions.AllowAny()]


@api_view(["POST"])
def uploadPRFByExcel(request):
    try:
        data = request.data
        for h in data:
            checkPrfExist = ImpPrf.objects.filter(
                Q(project_year=data[h].get("project_year"))
                & Q(project_name__iexact=data[h].get("project_name").strip().lower())
            )
            dateTime_UI = data[h].get("creatdate")
            userName = data[h].get("creater")
            # print(str(checkBudExist.query))
            if len(data[h].get("prf_ln")) != 0:
                prf_ln = data[h].get("prf_ln")
            else:
                prf_ln = []
            ## get model object for FK column
            # obj_handle_div = ImpDiv.objects.get(id=data[h].get("handle_div_id"))
            # obj_project_type = ProjType.objects.get(id=data[h].get("project_type_id"))
            # obj_project_category = ProjCategory.objects.get(id=data[h].get("project_category_id"))
            # obj_bu = ImpPrf.objects.get(id=data[h].get("bu_id"))
            ## set model object to FK column
            # h["handle_div"] = obj_handle_div
            # h["project_type"] = obj_project_type
            # h["project_category"] = obj_project_category
            # h["bu"] = obj_bu

            ## pop unused item
            if "id" in  data[h]:
                data[h].pop("id")
            if "bu_id" in  data[h]:
                data[h].pop("bu_id")
            if "handle_div_id" in  data[h]:
                data[h].pop("handle_div_id")
            if "project_category_id" in  data[h]:
                data[h].pop("project_category_id")
            if "project_type_id" in  data[h]:
                data[h].pop("project_type_id")
            if "prf_ln" in  data[h]:
                data[h].pop("prf_ln")
            if "bud_id" in  data[h]:
                data[h].pop("bud_id")
            if "user_name" in  data[h]:
                data[h].pop("user_name")

            if len(checkPrfExist):
                if "creatdate" in  data[h]:
                    data[h].pop("creatdate")
                if "creater" in  data[h]:
                    data[h].pop("creater")
                data[h]["updatedate"] = dateTime_UI
                data[h]["updater"] = userName
                print(data[h])
                obj_prf = ImpPrf.objects.filter(id=checkPrfExist.get().id).update(
                    **data[h]
                )
                obj_prf = checkPrfExist.get().id
            else:
                data[h]["creatdate"] = dateTime_UI
                data[h]["creater"] = userName
                if "updatedate" in  data[h]:
                    data[h].pop("updatedate")
                if "updater" in  data[h]:
                    data[h].pop("updater")
                print(data[h])
                obj_prf = ImpPrf.objects.create(**data[h])
                obj_prf = obj_prf.id

            project_year = data[h].get("project_year")
            project_name = data[h].get("project_name")

            if obj_prf and prf_ln is not None and len(prf_ln) != 0:
                ImpPrfln.objects.filter(
                    Q(project_year=data[h].get("project_year"))
                    & Q(
                        project_name__iexact=data[h].get("project_name").strip().lower()
                    )
                    & Q(prf_id=obj_prf)
                ).delete()
                for d in prf_ln:
                    checkPrfLnExist = ImpPrfln.objects.filter(
                        Q(project_year=data[h].get("project_year"))
                        & Q(project_name=data[h].get("project_name"))
                        & Q(div_group=d.get("div_group"))
                        & Q(prf_id=obj_prf)
                    )
                    d["prf_id"] = obj_prf
                    d["project_year"] = project_year
                    d["project_name"] = project_name
                    d["jan_plan"] = round(d["jan_plan"],2)
                    d["feb_plan"] = round(d["feb_plan"],2)
                    d["mar_plan"] = round(d["mar_plan"],2)
                    d["apr_plan"] = round(d["apr_plan"],2)
                    d["may_plan"] = round(d["may_plan"],2)
                    d["jun_plan"] = round(d["jun_plan"],2)
                    d["jul_plan"] = round(d["jul_plan"],2)
                    d["aug_plan"] = round(d["aug_plan"],2)
                    d["sep_plan"] = round(d["sep_plan"],2)
                    d["oct_plan"] = round(d["oct_plan"],2)
                    d["nov_plan"] = round(d["nov_plan"],2)
                    d["dec_plan"] = round(d["dec_plan"],2)
                    if "id" in d:
                        d.pop("id")
                    if "div_group_id" in d:
                        d.pop("div_group_id")
                    if "div_code" in d:
                        d.pop("div_code")
                    # if "div_group" in d:
                    #     d.pop("div_group")
                    if "colorRow" in d:
                        d.pop("colorRow")
                    if "index" in d:
                        d.pop("index")
                    print(d)

                    if len(checkPrfLnExist):
                        d["id"] = checkPrfLnExist.get().id
                        if "creatdate" in d:
                            d.pop("creatdate")
                        if "creater" in d:
                            d.pop("creater")
                        d["updatedate"] = dateTime_UI
                        d["updater"] = userName
                        obj_prfln = ImpPrfln.objects.filter(
                            id=checkPrfLnExist.get().id
                        ).update(**d)
                    else:
                        if "updatedate" in d:
                            d.pop("updatedate")
                        if "updater" in  d:
                            d.pop("updater")
                        d["creatdate"] = dateTime_UI
                        d["creater"] = userName
                        obj_prfln = ImpPrfln.objects.create(**d)
        if obj_prf is not None or obj_prfln is not None:
            return Response("OK")
        else:
            return Response("Fail")
    except Exception as e:
        print(e)
        return Response(traceback.format_exc())


@api_view(["POST"])
def index(request):
    try:
        data = request.data
        for h in data:
            checkBudExist = ImpBud.objects.filter(
                Q(project_year=data[h].get("project_year"))
                & Q(project_name__iexact=data[h].get("project_name").strip().lower())
            )
            if len(data[h].get("bud_plan")) != 0:
                bud_plan = data[h].get("bud_plan")
            else:
                bud_plan = []
            ## get model object for FK column
            obj_handle_div = ImpDiv.objects.get(id=data[h].get("handle_div_id"))
            obj_project_type = ProjType.objects.get(id=data[h].get("project_type_id"))
            obj_project_category = ProjCategory.objects.get(
                id=data[h].get("project_category_id")
            )
            obj_bu = ImpBu.objects.get(id=data[h].get("bu_id"))
            ## set model object to FK column
            # h["handle_div"] = obj_handle_div
            # h["project_type"] = obj_project_type
            # h["project_category"] = obj_project_category
            # h["bu"] = obj_bu

            ## pop unused item
            if "id" in data[h]:
                data[h].pop("id")
            if "bu_id" in data[h]:
                data[h].pop("bu_id")
            if "handle_div_id" in data[h]:
                data[h].pop("handle_div_id")
            if "project_category_id" in data[h]:
                data[h].pop("project_category_id")
            if "project_type_id" in data[h]:
                data[h].pop("project_type_id")
            if "bud_plan" in data[h]:
                data[h].pop("bud_plan")
            if "bud_id" in data[h]:
                data[h].pop("bud_id")

            if len(checkBudExist):
                obj_bud = ImpBud.objects.filter(id=checkBudExist.get().id).update(
                    **data[h]
                )
                obj_bud = checkBudExist.get().id
            else:
                print(data[h])
                obj_bud = ImpBud.objects.create(**data[h])
                obj_bud = obj_bud.id

            project_year = data[h].get("project_year")
            project_name = data[h].get("project_name")

            if obj_bud and bud_plan is not None and len(bud_plan) != 0:
                ImpBudln.objects.filter(
                    Q(project_year=data[h].get("project_year"))
                    & Q(
                        project_name__iexact=data[h].get("project_name").strip().lower()
                    )
                    & Q(bud_id=obj_bud)
                ).delete()
                for d in bud_plan:
                    checkBudLnExist = ImpBudln.objects.filter(
                        Q(project_year=data[h].get("project_year"))
                        & Q(
                            project_name__iexact=data[h]
                            .get("project_name")
                            .strip()
                            .lower()
                        )
                        & Q(resource=d.get("resource"))
                        & Q(bud_id=obj_bud)
                    )
                    d["bud_id"] = obj_bud
                    d["project_year"] = project_year
                    d["project_name"] = project_name
                    d["jan_plan"] = round(d["jan_plan"],2)
                    d["feb_plan"] = round(d["feb_plan"],2)
                    d["mar_plan"] = round(d["mar_plan"],2)
                    d["apr_plan"] = round(d["apr_plan"],2)
                    d["may_plan"] = round(d["may_plan"],2)
                    d["jun_plan"] = round(d["jun_plan"],2)
                    d["jul_plan"] = round(d["jul_plan"],2)
                    d["aug_plan"] = round(d["aug_plan"],2)
                    d["sep_plan"] = round(d["sep_plan"],2)
                    d["oct_plan"] = round(d["oct_plan"],2)
                    d["nov_plan"] = round(d["nov_plan"],2)
                    d["dec_plan"] = round(d["dec_plan"],2)
                    if "id" in d:
                        d.pop("id")
                    if "resource_id" in d:
                        d.pop("resource_id")
                    if "div_code" in d:
                        d.pop("div_code")
                    if "div_group" in d:
                        d.pop("div_group")
                    if "colorRow" in d:
                        d.pop("colorRow")
                    if "index" in d:
                        d.pop("index")
                    if len(checkBudLnExist):
                        d["id"] = checkBudLnExist.get().id
                    # d["resource"] = obj_resource
                    # d["project_year"] = project_year
                    # d["project_name"] = project_name
                    if len(checkBudLnExist):
                        obj_budln = ImpBudln.objects.filter(
                            id=checkBudLnExist.get().id
                        ).update(**d)
                    else:
                        obj_budln = ImpBudln.objects.create(**d)
        if obj_bud is not None or obj_budln is not None:
            return Response("OK")
        else:
            return Response("Fail")
    except:
        return Response(traceback.format_exc())

@swagger_auto_schema(
    method="post",
    operation_summary= "Get checking report api",
    operation_description= "",
    request_body= openapi.Schema(
        type= openapi.TYPE_OBJECT,
        properties={
            "project_year": openapi.Schema(type=openapi.TYPE_STRING, description="PRF Project Year"),
            "project_name": openapi.Schema(type=openapi.TYPE_STRING, description="PRF Project Name"),
            "ib_code": openapi.Schema(type=openapi.TYPE_STRING, description="IB Code"),
        }, required=["project_year","project_name","ib_code"]
    )
)
@api_view(["post"])
def getCheckingReport(request):
    try:
        sqlParameters = []
        data = request.data
        project_year = (data).get("project_year")
        project_name = (data).get("project_name")
        ib_code = (data).get("ib_code")
        # paj_number = (data).get("paj_number")
        COMMON_QUERY = """ WITH dt_piva AS (
	SELECT *
	FROM crosstab (
	   'SELECT akey,tssmonth2,tss_mm
		FROM tss_past_by_month
		ORDER BY 1,2,3
		'
	) AS ct ("akey" TEXT, "jan_plan" FLOAT8, "feb_plan" FLOAT8, "mar_plan" float8,"apr_plan" float8, "may_plan" float8,"jun_plan" float8,"jul_plan" float8,"aug_plan" float8,"sep_plan" float8,"oct_plan" float8,"nov_plan" float8,"dec_plan" FLOAT8)
),
dt_tss_past AS (
	SELECT
		tsspast.pmcs_ib_project_year || ';' || tsspast.pmcs_ib_project_name || ';' || tsspast.div_group || ';' || tsspast.ib_code AS akey,
		pmcs_ib_project_year, pmcs_ib_project_name, ib_code, it_pm, div_group
	FROM imp_tsspast tsspast
	GROUP BY tsspast.pmcs_ib_project_year || ';' || tsspast.pmcs_ib_project_name || ';' || tsspast.div_group || ';' || tsspast.ib_code, pmcs_ib_project_year, pmcs_ib_project_name, ib_code, it_pm, div_group
),
dt_tss AS (
	SELECT
		past.pmcs_ib_project_year AS project_year, past.pmcs_ib_project_name AS project_name, past.ib_code, past.it_pm, past.div_group ,
		main.jan_plan,	main.feb_plan,	main.mar_plan,	main.apr_plan,	main.may_plan,	main.jun_plan,	main.jul_plan,	main.aug_plan,	main.sep_plan,
		main.oct_plan, main.nov_plan, main.dec_plan
	FROM dt_piva main JOIN dt_tss_past past ON main.akey = past.akey
),
dt_prf AS (
	SELECT
		PRF.project_year, PRF.project_name, PRF.it_pm ,PRF.handle_div, PRF.mis_ib_code AS ib_code, PRFLN.div_group,
		PRFLN.jan_plan, PRFLN.feb_plan, PRFLN.mar_plan, PRFLN.apr_plan,
		PRFLN.may_plan, PRFLN.jun_plan, PRFLN.jul_plan, PRFLN.aug_plan,
		PRFLN.sep_plan, PRFLN.oct_plan, PRFLN.nov_plan, PRFLN.dec_plan
	FROM imp_prf PRF INNER JOIN imp_prfln PRFLN ON PRF.id = PRFLN.prf_id AND PRF.project_year = PRFLN.project_year AND PRF.project_name = PRFLN.project_name
),
dt_ib AS (
	SELECT
		IB.project_year, IB.project_name, IB.it_pm , IB.handle_div, IB.ib_code, IBLN.div_group,
		IBLN.jan_plan, IBLN.feb_plan, IBLN.mar_plan, IBLN.apr_plan,
		IBLN.may_plan, IBLN.jun_plan, IBLN.jul_plan, IBLN.aug_plan,
		IBLN.sep_plan, IBLN.oct_plan, IBLN.nov_plan, IBLN.dec_plan
	FROM imp_ib IB INNER JOIN imp_ibln IBLN ON IB.id = IBLN.ib_id  AND IB.project_year = IBLN.project_year AND IB.project_name = IBLN.project_name
),
dt_paj AS (
	SELECT
		PAJLN.project_year, PAJLN.project_name, PAJLN.div_group,PAJLN.ib_code,
		PAJLN.jan_plan, PAJLN.feb_plan, PAJLN.mar_plan, PAJLN.apr_plan,
		PAJLN.may_plan, PAJLN.jun_plan, PAJLN.jul_plan, PAJLN.aug_plan,
		PAJLN.sep_plan, PAJLN.oct_plan, PAJLN.nov_plan, PAJLN.dec_plan
	FROM imp_pajln PAJLN
)
	SELECT
		dt_prf.project_year, dt_prf.project_name, dt_prf.it_pm, dt_prf.handle_div, COALESCE(dt_ib.ib_code,'') AS ib_code,
		COALESCE(dt_prf.div_group,'') AS Div_Group_Budget,
		COALESCE(dt_prf.jan_plan,0) AS Jan_Budget, COALESCE(dt_prf.feb_plan,0) AS Feb_Budget, COALESCE(dt_prf.mar_plan,0) AS Mar_Budget, COALESCE(dt_prf.apr_plan,0) AS Apr_Budget,
		COALESCE(dt_prf.may_plan,0) AS May_Budget, COALESCE(dt_prf.jun_plan,0) AS Jun_Budget, COALESCE(dt_prf.jul_plan,0) AS Jul_Budget, COALESCE(dt_prf.aug_plan,0) AS Aug_Budget,
		COALESCE(dt_prf.sep_plan,0) AS Sep_Budget, COALESCE(dt_prf.oct_plan,0) AS Oct_Budget, COALESCE(dt_prf.nov_plan,0) AS Nov_Budget, COALESCE(dt_prf.dec_plan,0) AS Dec_Budget,
		COALESCE(dt_ib.div_group,'') AS Div_Group_Plan,
		COALESCE(dt_ib.jan_plan,0) AS Jan_Plan, COALESCE(dt_ib.feb_plan,0) AS Feb_Plan, COALESCE(dt_ib.mar_plan,0) AS Mar_Plan, COALESCE(dt_ib.apr_plan,0) AS Apr_Plan,
		COALESCE(dt_ib.may_plan,0) AS May_Plan, COALESCE(dt_ib.jun_plan,0) AS Jun_Plan, COALESCE(dt_ib.jul_plan,0) AS Jul_Plan, COALESCE(dt_ib.aug_plan,0) AS Aug_Plan,
		COALESCE(dt_ib.sep_plan,0) AS Sep_Plan, COALESCE(dt_ib.oct_plan,0) AS Oct_Plan, COALESCE(dt_ib.nov_plan,0) AS Nov_Plan, COALESCE(dt_ib.dec_plan,0) AS Dec_Plan,
		COALESCE(dt_paj.div_group,'') AS Div_Group_PAJ,
		COALESCE(dt_paj.jan_plan,0) AS Jan_PAJ, COALESCE(dt_paj.feb_plan,0) AS Feb_PAJ, COALESCE(dt_paj.mar_plan,0) AS Mar_PAJ, COALESCE(dt_paj.apr_plan,0) AS Apr_PAJ,
		COALESCE(dt_paj.may_plan,0) AS May_PAJ, COALESCE(dt_paj.jun_plan,0) AS Jun_PAJ, COALESCE(dt_paj.jul_plan,0) AS Jul_PAJ,COALESCE(dt_paj.aug_plan,0) AS Aug_PAJ,
		COALESCE(dt_paj.sep_plan,0) AS Sep_PAJ, COALESCE(dt_paj.oct_plan,0) AS Oct_PAJ, COALESCE(dt_paj.nov_plan,0) AS Nov_PAJ, COALESCE(dt_paj.dec_plan,0) AS Dec_PAJ,
		COALESCE(dt_tss.div_group,'') AS Div_Group_TSS,
		COALESCE(dt_tss.jan_plan,0) AS Jan_TSS, COALESCE(dt_tss.feb_plan,0) AS Feb_TSS, COALESCE(dt_tss.mar_plan,0) AS Mar_TSS, COALESCE(dt_tss.apr_plan,0) AS Apr_TSS,
		COALESCE(dt_tss.may_plan,0) AS May_TSS, COALESCE(dt_tss.jun_plan,0) AS Jun_TSS, COALESCE(dt_tss.jul_plan,0) AS Jul_TSS,COALESCE(dt_tss.aug_plan,0) AS Aug_TSS,
		COALESCE(dt_tss.sep_plan,0) AS Sep_TSS, COALESCE(dt_tss.oct_plan,0) AS Oct_TSS, COALESCE(dt_tss.nov_plan,0) AS Nov_TSS, COALESCE(dt_tss.dec_plan,0) AS Dec_TSS
	FROM dt_prf LEFT JOIN dt_ib
			ON dt_prf.project_year = dt_ib.project_year AND dt_prf.project_name = dt_ib.project_name AND dt_prf.div_group = dt_ib.div_group
		LEFT JOIN dt_paj
			ON dt_ib.project_year = dt_paj.project_year AND dt_ib.project_name = dt_paj.project_name AND dt_ib.ib_code = dt_paj.ib_code AND dt_ib.div_group = dt_paj.div_group
		LEFT JOIN dt_tss
			ON dt_paj.project_year = dt_tss.project_year AND dt_paj.project_name = dt_tss.project_name AND dt_paj.ib_code = dt_tss.ib_code AND dt_paj.div_group = dt_tss.div_group
	WHERE 1=1 """
        PY_QUERY = "AND dt_prf.project_year = %s "
        PN_QUERY = "AND UPPER(dt_prf.project_name) LIKE UPPER(%s) "
        IB_QUERY = "AND UPPER(dt_ib.ib_code) LIKE UPPER (%s) "
        COMMON_ORDER = "ORDER BY dt_prf.project_year, dt_prf.project_name, dt_prf.it_pm, dt_prf.handle_div ASC"
        with connection.cursor() as cursor:
            if project_year:
                COMMON_QUERY = COMMON_QUERY + PY_QUERY
                sqlParameters.append(project_year)
            if project_name:
                COMMON_QUERY = COMMON_QUERY + PN_QUERY
                sqlParameters.append("%" + project_name + "%")
            if ib_code:
                COMMON_QUERY = COMMON_QUERY + IB_QUERY
                sqlParameters.append("%" + ib_code + "%")
            cursor.execute(COMMON_QUERY + COMMON_ORDER, sqlParameters)
            result = namedtuplefetchall_CheckingReport(cursor)
        return Response(result)
    except (TypeError, AttributeError) as e:
        traceback.print_exc(e)
        return Response(traceback.format_exc(e))

def adjust12MonthlyPlan(gola_Target, target_Word = "", rounding_Number = 0):
    months = list(calendar.month_abbr)
    months.pop("")
    for month in months:
        adjusted_element = month.lower() + target_Word
        adjusted_value = round(gola_Target[adjusted_element],rounding_Number)
        gola_Target[adjusted_element] = adjusted_value

def namedtuplefetchall_CheckingReport(cursor):
    # Return all rows from a cursor as a namedtuple
    # desc = cursor.description
    nt_result = namedtuple(
        "Result",
        ["project_year", "project_name", "it_pm", "handle_div", "ib_code",
         "Div_Group_Budget",
         "Jan_Budget", "Feb_Budget", "Mar_Budget", "Apr_Budget", "May_Budget", "Jun_Budget",
         "Jul_Budget", "Aug_Budget", "Sep_Budget", "Oct_Budget", "Nov_Budget", "Dec_Budget",
         "Div_Group_Plan",
         "Jan_Plan", "Feb_Plan", "Mar_Plan", "Apr_Plan", "May_Plan", "Jun_Plan",
         "Jul_Plan", "Aug_Plan", "Sep_Plan", "Oct_Plan", "Nov_Plan", "Dec_Plan",
         "Div_Group_PAJ",
         "Jan_PAJ", "Feb_PAJ", "Mar_PAJ", "Apr_PAJ", "May_PAJ", "Jun_PAJ",
         "Jul_PAJ", "Aug_PAJ", "Sep_PAJ", "Oct_PAJ", "Nov_PAJ", "Dec_PAJ",
         "Div_Group_TSS",
         "Jan_TSS", "Feb_TSS", "Mar_TSS", "Apr_TSS", "May_TSS", "Jun_TSS",
         "Jul_TSS", "Aug_TSS", "Sep_TSS", "Oct_TSS", "Nov_TSS", "Dec_TSS"],
    )
    result = [nt_result(*row) for row in cursor.fetchall()]
    result = [
        {"project_year": r.project_year,
        "project_name": r.project_name,
        "it_pm": r.it_pm,
        "handle_div": r.handle_div,
        "ib_code": r.ib_code,
        "Div_Group_Budget": r.Div_Group_Budget,
        "Jan_Budget": r.Jan_Budget, "Feb_Budget":r.Feb_Budget, "Mar_Budget":r.Mar_Budget, "Apr_Budget":r.Apr_Budget, "May_Budget":r.May_Budget, "Jun_Budget":r.Jun_Budget,"Jul_Budget": r.Jul_Budget, "Aug_Budget":r.Aug_Budget, "Sep_Budget":r.Sep_Budget, "Oct_Budget":r.Oct_Budget, "Nov_Budget":r.Nov_Budget, "Dec_Budget":r.Dec_Budget,
        "Div_Group_Plan": r.Div_Group_Plan,
        "Jan_Plan": r.Jan_Plan, "Feb_Plan": r.Feb_Plan, "Mar_Plan": r.Mar_Plan, "Apr_Plan": r.Apr_Plan, "May_Plan": r.May_Plan, "Jun_Plan": r.Jun_Plan,"Jul_Plan": r.Jul_Plan, "Aug_Plan": r.Aug_Plan, "Sep_Plan": r.Sep_Plan, "Oct_Plan": r.Oct_Plan, "Nov_Plan": r.Nov_Plan, "Dec_Plan": r.Dec_Plan,
        "Div_Group_PAJ": r.Div_Group_PAJ,
        "Jan_PAJ": r.Jan_PAJ, "Feb_PAJ": r.Feb_PAJ, "Mar_PAJ": r.Mar_PAJ, "Apr_PAJ": r.Apr_PAJ, "May_PAJ": r.May_PAJ, "Jun_PAJ": r.Jun_PAJ,"Jul_PAJ": r.Jul_PAJ, "Aug_PAJ": r.Aug_PAJ, "Sep_PAJ": r.Sep_PAJ, "Oct_PAJ": r.Oct_PAJ, "Nov_PAJ": r.Nov_PAJ, "Dec_PAJ": r.Dec_PAJ,
        "Div_Group_TSS": r.Div_Group_TSS,
        "Jan_TSS": r.Jan_TSS, "Feb_TSS": r.Feb_TSS, "Mar_TSS": r.Mar_TSS, "Apr_TSS": r.Apr_TSS, "May_TSS": r.May_TSS, "Jun_TSS": r.Jun_TSS,
        "Jul_TSS": r.Jul_TSS, "Aug_TSS": r.Aug_TSS, "Sep_TSS": r.Sep_TSS, "Oct_TSS": r.Oct_TSS, "Nov_TSS": r.Nov_TSS, "Dec_TSS": r.Dec_TSS}
        for r in result
    ]
    return result

@swagger_auto_schema(
    method='post',
    operation_description="Convert PRF to IB",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
           "0": openapi.Schema(type=openapi.TYPE_OBJECT, description="Copy PRF to IB datas,eg..0,1,2,3...",
           properties={
                "project_year": openapi.Schema(type=openapi.TYPE_STRING, description="Budget Project Year"),
                "project_name": openapi.Schema(type=openapi.TYPE_STRING, description="Budget Project Name"),
                "user_name": openapi.Schema(type=openapi.TYPE_STRING, description="User Name"),
           }, required=["project_year","project_name","user_name"])
        }
    ),
)
@api_view(["post"])
def copyPRF2IB(request):
    try:
        datas = request.data
        for data in datas:
            checkIBExist = ImpIb.objects.filter(
                Q(project_year=datas[data].get("project_year"))
                & Q(project_name=datas[data].get("project_name"))
            )

            if len(checkIBExist):
                ImpIb.objects.filter(id=checkIBExist[0].id).delete()
                ImpIbln.objects.filter(ib_id=checkIBExist[0].id).delete()

            prf = getPRF4IB(
                datas[data].get("project_year"), datas[data].get("project_name")
            )
            imp_IB = {}
            imp_IB["project_year"] = str(prf[0]["project_year"])
            imp_IB["project_name"] = str(prf[0]["project_name"])
            imp_IB["it_pm"] = str(prf[0]["it_pm"])
            imp_IB["plan_start"] = str(prf[0]["plan_start"])
            imp_IB["plan_finish"] = str(prf[0]["plan_finish"])
            imp_IB["ib_code"] = str(prf[0]["mis_ib_code"])
            imp_IB["pmcs_ib_project_name"] = str(prf[0]["pmcs_ib_project_name"])
            imp_IB["ep_code"] = str(prf[0]["mis_ep_code"])
            imp_IB["pmcs_ep_project_name"] = str(prf[0]["pmcs_ep_project_name"])
            imp_IB["handle_div"] = str(prf[0]["handle_div"])
            imp_IB["cancelled"] = str(prf[0]["cancelled"])
            imp_IB["complete"] = str(prf[0]["complete"])
            imp_IB["monthly_paj_done"] = "N"
            imp_IB["creater"] = str(datas[data].get("user_name"))
            imp_IB["creatdate"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ib_new_id = ImpIb.objects.create(**imp_IB)

            IBLNs_list_to_insert = []
            prflns = getPRFLN4IB(
                datas[data].get("project_year"), datas[data].get("project_name")
            )
            for i in range(0, len(prflns)):
                impIBLNs = ImpIbln(
                    project_year=str(prflns[i]["project_year"]),
                    project_name=str(prflns[i]["project_name"]),
                    jan_plan=float(prflns[i]["jan_plan"]),
                    feb_plan=float(prflns[i]["feb_plan"]),
                    mar_plan=float(prflns[i]["mar_plan"]),
                    apr_plan=float(prflns[i]["apr_plan"]),
                    may_plan=float(prflns[i]["may_plan"]),
                    jun_plan=float(prflns[i]["jun_plan"]),
                    jul_plan=float(prflns[i]["jul_plan"]),
                    aug_plan=float(prflns[i]["aug_plan"]),
                    sep_plan=float(prflns[i]["sep_plan"]),
                    oct_plan=float(prflns[i]["oct_plan"]),
                    nov_plan=float(prflns[i]["nov_plan"]),
                    dec_plan=float(prflns[i]["dec_plan"]),
                    div_group=str(prflns[i]["div_group"]),
                    ib_id=ib_new_id.id,
                    creatdate=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    creater=str(datas[data].get("user_name")),
                )
                IBLNs_list_to_insert.append(impIBLNs)
            ImpIbln.objects.bulk_create(IBLNs_list_to_insert)
            response = {
                "project_year": datas[data].get("project_year"),
                "project_name": datas[data].get("project_name"),
            }
        return Response(response)
    except (TypeError, AttributeError) as e:
        traceback.print_exc(e)
        return Response(traceback.format_exc(e))


def getPRF4IB(project_year, project_name):
    COMMON_QUERY = """SELECT PRF.project_year, PRF.project_name, PRF.it_pm, PRF.plan_start, PRF.plan_finish, PRF.mis_ib_code, PRF.pmcs_ib_project_name, PRF.mis_ep_code, PRF.pmcs_ep_project_name, PRF.cancelled, PRF.complete, PRF.handle_div FROM imp_prf PRF WHERE PRF.project_year = %s AND PRF.project_name = %s"""
    COMMON_ORDER = " ORDER BY PRF.project_year, PRF.project_name ASC"
    with connection.cursor() as cursor:
        cursor.execute(COMMON_QUERY + COMMON_ORDER, [project_year, project_name])
        result = namedtuplefetchallIB(cursor)
        return result


def namedtuplefetchallIB(cursor):
    # Return all rows from a cursor as a namedtuple
    # desc = cursor.description
    nt_result = namedtuple(
        "Result",
        [
            "project_year",
            "project_name",
            "it_pm",
            "plan_start",
            "plan_finish",
            "mis_ib_code",
            "pmcs_ib_project_name",
            "mis_ep_code",
            "pmcs_ep_project_name",
            "cancelled",
            "complete",
            "handle_div",
        ],
    )
    result = [nt_result(*row) for row in cursor.fetchall()]
    result = [
        {
            "project_year": r.project_year,
            "project_name": r.project_name,
            "it_pm": r.it_pm,
            "plan_start": r.plan_start,
            "plan_finish": r.plan_finish,
            "mis_ib_code": r.mis_ib_code,
            "pmcs_ib_project_name": r.project_name,
            "mis_ep_code": r.mis_ep_code,
            "pmcs_ep_project_name": r.project_name,
            "cancelled": r.cancelled,
            "complete": r.complete,
            "handle_div": r.handle_div,
        }
        for r in result
    ]
    return result


def getPRFLN4IB(project_year, project_name):
    COMMON_QUERY = """SELECT PRF.project_year, PRF.project_name, PRF.div_group, PRF.jan_plan, PRF.feb_plan, PRF.mar_plan, PRF.apr_plan, PRF.may_plan, PRF.jun_plan, PRF.jul_plan, PRF.aug_plan, PRF.sep_plan, PRF.oct_plan, PRF.nov_plan, PRF.dec_plan FROM imp_prfln PRF WHERE PRF.project_year = %s AND PRF.project_name = %s"""
    COMMON_ORDER = " ORDER BY PRF.project_year, PRF.project_name ASC"
    with connection.cursor() as cursor:
        cursor.execute(COMMON_QUERY + COMMON_ORDER, [project_year, project_name])
        result = namedtuplefetchallIBLN(cursor)
        return result


def namedtuplefetchallIBLN(cursor):
    # Return all rows from a cursor as a namedtuple
    # desc = cursor.description
    nt_result = namedtuple(
        "Result",
        [
            "project_year",
            "project_name",
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
            "project_year": r.project_year,
            "project_name": r.project_name,
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
            "dec_plan": r.dec_plan,
        }
        for r in result
    ]
    return result


@swagger_auto_schema(
    method='post',
    operation_description="Convert budget projetc to PRF",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
           "0": openapi.Schema(type=openapi.TYPE_OBJECT, description="Copy budget project to PRF datas,eg..0,1,2,3...",
           properties={
                "project_year": openapi.Schema(type=openapi.TYPE_STRING, description="Budget Project Year"),
                "project_name": openapi.Schema(type=openapi.TYPE_STRING, description="Budget Project"),
                "user_name": openapi.Schema(type=openapi.TYPE_STRING, description="User Name"),
           }, required=["project_year","project_name","user_name"])
        }
    ),
)
@api_view(["post"])
def copyBud2PRF(request):
    try:
        datas = request.data
        for data in datas:
            checkPrfExist = ImpPrf.objects.filter(
                Q(project_year=datas[data].get("project_year"))
                & Q(project_name=datas[data].get("project_name"))
            )
            if len(checkPrfExist):
                ImpPrf.objects.filter(id=checkPrfExist[0].id).delete()
                ImpPrfln.objects.filter(prf_id=checkPrfExist[0].id).delete()

            bud = getBudheader4PRF(
                datas[data].get("project_year"), datas[data].get("project_name")
            )
            if len(bud) :
                imp_PRF = {}
                imp_PRF["project_year"] = str(bud[0]["project_year"])
                imp_PRF["project_name"] = str(bud[0]["project_name"])
                imp_PRF["it_pm"] = str(bud[0]["it_pm"])
                imp_PRF["biz_owner"] = str(bud[0]["biz_owner"])
                imp_PRF["contact_window"] = str(bud[0]["contact_window"])
                imp_PRF["bu"] = str(bud[0]["bu"])
                imp_PRF["bg"] = str(bud[0]["bg"])
                imp_PRF["bo"] = str(bud[0]["bo"])
                imp_PRF["customer"] = str(bud[0]["customer"])
                imp_PRF["site"] = str(bud[0]["site"])
                imp_PRF["plan_start"] = bud[0]["plan_start"]
                imp_PRF["plan_finish"] = bud[0]["plan_finish"]
                imp_PRF["recv_ep_code"] = str(bud[0]["recv_ep_code"])
                imp_PRF["recv_chg_dept"] = str(bud[0]["recv_chg_dept"])
                imp_PRF["bud_syst_recv_chg_dept"] = str(bud[0]["bud_syst_recv_chg_dept"])
                imp_PRF["project_category"] = str(bud[0]["project_category"])
                imp_PRF["project_type"] = str(bud[0]["project_type"])
                imp_PRF["handle_div"] = str(bud[0]["handle_div"])
                imp_PRF["comments"] = str(bud[0]["comments"])
                imp_PRF["mis_handle_div_group"] = str(bud[0]["mis_handle_div_group"])
                imp_PRF["mis_ib_code"] = ""
                imp_PRF["pmcs_ib_project_name"] = str(bud[0]["pmcs_ib_project_name"])
                imp_PRF["mis_ep_code"] = ""
                imp_PRF["pmcs_ep_project_name"] = str(bud[0]["pmcs_ep_project_name"])
                imp_PRF["cancelled"] = "N"
                imp_PRF["complete"] = "N"
                imp_PRF["split"] = float(100.0)
                imp_PRF["creater"] = str(datas[data].get("user_name"))
                imp_PRF["creatdate"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                prf_new_id = ImpPrf.objects.create(**imp_PRF)

                PRFLNs_list_to_insert = []
                budlns = getBudplan4PRFLN(
                    datas[data].get("project_year"), datas[data].get("project_name")
                )
                if len(budlns):
                    for i in range(0, len(budlns)):
                        impPRFLNs = ImpPrfln(
                            project_year=str(budlns[i]["project_year"]),
                            project_name=str(budlns[i]["project_name"]),
                            jan_plan=float(budlns[i]["jan_plan"]),
                            feb_plan=float(budlns[i]["feb_plan"]),
                            mar_plan=float(budlns[i]["mar_plan"]),
                            apr_plan=float(budlns[i]["apr_plan"]),
                            may_plan=float(budlns[i]["may_plan"]),
                            jun_plan=float(budlns[i]["jun_plan"]),
                            jul_plan=float(budlns[i]["jul_plan"]),
                            aug_plan=float(budlns[i]["aug_plan"]),
                            sep_plan=float(budlns[i]["sep_plan"]),
                            oct_plan=float(budlns[i]["oct_plan"]),
                            nov_plan=float(budlns[i]["nov_plan"]),
                            dec_plan=float(budlns[i]["dec_plan"]),
                            div_group=str(budlns[i]["div_group"]),
                            prf_id=prf_new_id.id,
                            creatdate=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            creater=str(datas[data].get("user_name")),
                        )
                        PRFLNs_list_to_insert.append(impPRFLNs)
                    ImpPrfln.objects.bulk_create(PRFLNs_list_to_insert)
            response = {
                "project_year": datas[data].get("project_year"),
                "project_name": datas[data].get("project_name"),
            }
        return Response(response)
    except (TypeError, AttributeError) as e:
        traceback.print_exc(e)
        return Response(traceback.format_exc(e))


def getBudheader4PRF(project_year, project_name):
    COMMON_QUERY = """SELECT BUD.project_year, BUD.project_name, BUD.it_pm, BUD.biz_owner, BUD.contact_window, BUD.customer, BUD.site, BUD.plan_start, BUD.plan_finish, BUD.recv_ep_code, BUD.comments, BUD.cancelled ,BUD.bud_syst_recv_chg_dept, BUD.bu, BUD.project_category, BUD.project_type, BUD.recv_chg_dept, BUD.project_name AS pmcs_ep_project_name, BUD.project_name AS pmcs_ib_project_name, DIV.div_group AS mis_handle_div_group, BUD.handle_div,BGBUBO.bg , BGBUBO.bo FROM imp_bud BUD, (SELECT BU.bu, BG.bg, BO.bo FROM imp_bu BU, imp_bo bo, imp_bg bg WHERE BU.bg_id = bg.id AND BU.bo_id = BO.id) BGBUBO, imp_div DIV WHERE BUD.bu = BGBUBO.bu AND BUD.handle_div = DIV.div AND BUD.project_year = %s AND BUD.project_name = %s"""
    COMMON_ORDER = " ORDER BY BUD.project_year, BUD.project_name ASC"
    with connection.cursor() as cursor:
        cursor.execute(COMMON_QUERY + COMMON_ORDER, [project_year, project_name])
        result = namedtuplefetchallPRF(cursor)
        return result


def namedtuplefetchallPRF(cursor):
    # Return all rows from a cursor as a namedtuple
    # desc = cursor.description
    nt_result = namedtuple(
        "Result",
        [
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
            "bud_syst_recv_chg_dept",
            "bu",
            "project_category",
            "project_type",
            "recv_chg_dept",
            "pmcs_ep_project_name",
            "pmcs_ib_project_name",
            "mis_handle_div_group",
            "handle_div",
            "bg",
            "bo",
        ],
    )
    result = [nt_result(*row) for row in cursor.fetchall()]
    result = [
        {
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
            "bud_syst_recv_chg_dept": r.bud_syst_recv_chg_dept,
            "bu": r.bu,
            "project_category": r.project_category,
            "project_type": r.project_type,
            "recv_chg_dept": r.recv_chg_dept,
            "pmcs_ep_project_name": r.project_name,
            "pmcs_ib_project_name": r.project_name,
            "mis_handle_div_group": r.mis_handle_div_group,
            "handle_div": r.handle_div,
            "bg": r.bg,
            "bo": r.bo,
        }
        for r in result
    ]
    return result


def getBudplan4PRFLN(project_year, project_name):
    COMMON_QUERY = """SELECT BUDLN.project_year, BUDLN.project_name, sum(BUDLN.jan_plan) AS jan_plan, sum(BUDLN.feb_plan) AS feb_plan, sum(BUDLN.mar_plan) AS mar_plan,
sum(BUDLN.apr_plan) AS apr_plan, sum(BUDLN.may_plan) AS may_plan, sum(BUDLN.jun_plan) AS jun_plan, sum(BUDLN.jul_plan) AS jul_plan,
sum(BUDLN.aug_plan) AS aug_plan, sum(BUDLN.sep_plan) AS sep_plan, sum(BUDLN.oct_plan) AS oct_plan, sum(BUDLN.nov_plan) AS nov_plan,
sum(BUDLN.dec_plan) AS dec_plan, RES.div_group
FROM imp_budln BUDLN LEFT JOIN (SELECT A.resource_group, B.div_group, B.div AS div_code
FROM imp_resource A, imp_div B WHERE A.div_group_id = B.id) RES ON UPPER(BUDLN.resource) = UPPER(RES.resource_group) WHERE BUDLN.project_year = %s AND BUDLN.project_name = %s """
    COMMON_ORDER = "GROUP BY BUDLN.project_year, BUDLN.project_name, RES.div_group"
    with connection.cursor() as cursor:
        cursor.execute(COMMON_QUERY + COMMON_ORDER, [project_year, project_name])
        result = namedtuplefetchallPRFLN(cursor)
        return result


def namedtuplefetchallPRFLN(cursor):
    # Return all rows from a cursor as a namedtuple
    # desc = cursor.description
    nt_result = namedtuple(
        "Result",
        [
            "project_year",
            "project_name",
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
        ],
    )
    result = [nt_result(*row) for row in cursor.fetchall()]
    result = [
        {
            "project_year": r.project_year,
            "project_name": r.project_name,
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
        }
        for r in result
    ]
    return result


@api_view(["post"])
def getBudIdnBudLnId(request):
    data = request.data
    project_year = (data).get("project_year")
    project_name = (data).get("project_name").strip().lower()

    getBudDatas = ImpBud.objects.filter(
        Q(project_year=project_year) & Q(project_name__iexact=project_name)
    )
    if len(getBudDatas):
        getBudLnDatas = ImpBudln.objects.filter(
            Q(project_year=project_year)
            & Q(project_name__iexact=project_name)
            & Q(bud=getBudDatas.get().id)
        )
        if len(getBudLnDatas):
            tmp = {
                "id": getBudDatas.get().id,
                "project_year": getBudDatas.get().project_year,
                "project_name": getBudDatas.get().project_name,
                "plan": [],
            }
            for d in getBudLnDatas:
                tmp["plan"].append(
                    {"id": d.id, "bud_id": d.bud_id, "resource_id": d.resource_id}
                )
            return JsonResponse(tmp)
        else:
            tmp = {
                "id": getBudDatas.get().id,
                "project_year": getBudDatas.get().project_year,
                "project_name": getBudDatas.get().project_name,
                "bud": [],
            }
            return JsonResponse(tmp)
    else:
        return Response([])

@swagger_auto_schema(
    method='post',
    operation_description="Create account, when the user first time log in IMP",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "id": openapi.Schema(type=openapi.TYPE_STRING, description="User Id"),
            "email": openapi.Schema(type=openapi.TYPE_STRING, description="Wistron's e-mail"),
        },
    ),
)
@api_view(["post"])
def create_user(request):
    try:
        req = request.data
        id = req.get("id")  # 工號
        email = req.get("email")
        password = "0000"
        userExist = User.objects.filter(Q(username=id) & Q(email=email))
        if len(userExist) > 0:
            COMMON_QUERY = """SELECT A.id, A.username, A.email, C.name AS groupname FROM auth_user A, auth_user_groups B, auth_group C
 WHERE A.ID = B.user_id AND B.group_id = C.ID AND (UPPER(A.username) = UPPER(%s) AND UPPER(A.email) = UPPER(%s))"""
            with connection.cursor() as cursor:
                cursor.execute(COMMON_QUERY, [id, email])
                result = namedtuplefetchall(cursor)
            result = {
                "id": userExist.get().username,
                "email": userExist.get().email,
                "groupname": result[0]["groupname"],
            }
            return JsonResponse(result)
        else:
            user = User.objects.create_user(username=id, email=email, password=password)
            user.is_staff = False
            group = Group.objects.get(name="VISITOR")
            user.groups.add(group)
            user.save()
            result = {
                "id": id,
                "email": email,
                "groupname": "VISITOR",
            }
            return JsonResponse(result)
    except:
        return Response("User existed")


def namedtuplefetchall(cursor):
    # Return all rows from a cursor as a namedtuple
    # desc = cursor.description
    nt_result = namedtuple(
        "Result",
        ["id", "username", "email", "groupname"],
    )
    result = [nt_result(*row) for row in cursor.fetchall()]
    result = [
        {"id": r.id, "username": r.username, "email": r.email, "groupname": r.groupname}
        for r in result
    ]
    return result
