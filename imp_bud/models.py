from django.db import models
from imp_bu.models import ImpBu
from imp_dept.models import ImpDept
from imp_projcategory.models import ProjCategory
from imp_projtype.models import ProjType
from imp_div.models import ImpDiv

# Create your models here.
class ImpBud(models.Model):
    id = models.AutoField(primary_key=True)
    project_year = models.CharField(
        null=False,
        max_length=4,
        default="",
        help_text="Project Year",
    )
    project_name = models.CharField(
        null=False,
        max_length=100,
        default="",
        help_text="Project Name",
    )
    it_pm = models.CharField(
        null=False,
        blank=True,
        max_length=50,
        default="",
        help_text="Project IT PM",
    )
    biz_owner = models.CharField(
        null=False,
        blank=True,
        max_length=50,
        default="",
        help_text="Project Biz Owner",
    )
    contact_window = models.CharField(
        null=False,
        blank=True,
        max_length=50,
        default="",
        help_text="Project Contact Window",
    )
    bu = models.CharField(
        max_length=20,
        default="",
        help_text="BU Names",
    )
    # bu = models.ForeignKey(
    #     ImpBu,
    #     on_delete=models.CASCADE,
    # )
    customer = models.CharField(
        null=True,
        blank=True,
        max_length=10,
        default="",
        help_text="Project Customer",
    )
    site = models.CharField(
        null=False,
        blank=True,
        max_length=20,
        default="",
    )
    plan_start = models.DateField(
        null=False,
    )
    plan_finish = models.DateField(
        null=False,
    )
    recv_ep_code = models.CharField(
        null=False,
        blank=True,
        max_length=20,
        default="",
        help_text="EP Code",
    )
    recv_chg_dept = models.CharField(
        null=False,
        blank=True,
        max_length=10,
        default="",
        help_text="Recv Charge Dept",
    )
    bud_syst_recv_chg_dept = models.CharField(
        null=False,
        blank=True,
        max_length=10,
        default="",
        help_text="Budget Syst Recv Charge Dept",
    )
    project_category = models.CharField(
        null=False,
        max_length=30,
        default="",
        help_text="Projectg Category",
    )
    # project_category = models.ForeignKey(
    #     ProjCategory,
    #     on_delete=models.CASCADE,
    #     help_text="Project Category ID",
    # )
    project_type = models.CharField(
        null=False,
        max_length=30,
        default="",
        help_text="Projectg Type",
    )
    # project_type = models.ForeignKey(
    #     ProjType,
    #     on_delete=models.CASCADE,
    #     help_text="Project Type ID",
    # )
    handle_div = models.CharField(
        null=False,
        max_length=20,
        default="",
        help_text="Division Code",
    )
    # handle_div = models.ForeignKey(
    #     ImpDiv,
    #     on_delete=models.CASCADE,
    #     help_text="Division ID",
    # )
    comments = models.CharField(
        null=True,
        blank=True,
        max_length=300,
        help_text="Project Comments",
    )
    cancelled = models.CharField(
        null=False,
        max_length=1,
        default="N",
        help_text="Project Cancelled",
    )

    class Meta:
        db_table = "imp_bud"
        unique_together = ("id", "project_year", "project_name")
        ordering = ['project_year', 'project_name', 'cancelled']
