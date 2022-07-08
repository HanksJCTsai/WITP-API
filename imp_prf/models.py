from django.db import models
# Create your models here.
class ImpPrf(models.Model):
    id = models.AutoField(
        primary_key=True,
    )

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
        max_length=50,
        default="",
        help_text="Project Biz Owner",
    )

    contact_window = models.CharField(
        null=False,
        max_length=50,
        default="",
        help_text="Project Contact Window",
    )

    bu = models.CharField(
        max_length=20,
        default="",
        help_text="BU Names",
    )

    bg = models.CharField(
        max_length=20,
        default="",
        help_text="BG Names",
    )

    bo = models.CharField(
        max_length=20,
        default="",
        help_text="BO Names",
    )

    customer = models.CharField(
        null=True,
        blank=True,
        max_length=50,
        default="",
        help_text="Project Customer",
    )

    site = models.CharField(
        null=False,
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
        null=True,
        blank=True,
        max_length=20,
        default="",
        help_text="EP Code",
    )

    recv_chg_dept = models.CharField(
        null=True,
        blank=True,
        max_length=10,
        default="",
        help_text="Recv Charge Dept",
    )

    bud_syst_recv_chg_dept = models.CharField(
        null=True,
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

    project_type = models.CharField(
        null=False,
        max_length=30,
        default="",
        help_text="Projectg Type",
    )

    handle_div = models.CharField(
        null=False,
        max_length=20,
        default="",
        help_text="Division Code",
    )

    comments = models.CharField(
        null=True,
        blank=True,
        max_length=300,
        help_text="Project Comments",
    )

    mis_handle_div_group = models.CharField(
        null=False,
        max_length=20,
        default="",
        help_text="MIS Handle Division Code",
    )

    mis_ib_code = models.CharField(
        null=True,
        blank=True,
        max_length=20,
        default="",
        help_text="IB Code",
    )

    pmcs_ib_project_name = models.CharField(
        null=False,
        max_length=100,
        default="",
        help_text="IB Project Name",
    )

    mis_ep_code = models.CharField(
        null=True,
        blank= True,
        max_length=20,
        default="",
        help_text="MIS EP Code",
    )

    pmcs_ep_project_name = models.CharField(
        null=False,
        max_length=100,
        default="",
        help_text="EP Project Name",
    )

    cancelled = models.CharField(
        null=False,
        max_length=1,
        default="N",
        help_text="Project Cancelled",
    )

    complete = models.CharField(
        null=False,
        max_length=1,
        default="N",
        help_text="Project Completed",
    )

    split = models.FloatField(
        null=False,
        default=100.0,
        help_text="Project Split Percentage",
    )

    creater = models.CharField(
        null=True,
        blank=True,
        max_length=50,
        default="",
        help_text="PRF Creater",
    )

    creatdate = models.DateTimeField(
        null=True,
        blank=True,
    )

    updater = models.CharField(
        null=True,
        blank=True,
        max_length=50,
        default="",
        help_text="PRF Updater",
    )

    updatedate = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "imp_prf"
        unique_together = ("id", "project_year", "project_name")
