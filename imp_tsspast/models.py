from django.db import models
from imp_div.models import ImpDiv

# Create your models here.
class ImpTssPast(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    pmcs_ib_project_year = models.CharField(
        null=False,
        max_length=4,
        default="",
        help_text="IB Project Year",
    )
    pmcs_ib_project_name = models.CharField(
        null=False,
        max_length=100,
        default="",
        help_text="IB Project Name",
    )
    ib_code = models.CharField(
        null=False,
        max_length=12,
        default="",
        help_text="IB Code",
    )
    it_pm = models.CharField(
        null=False,
        max_length=50,
        default="",
        help_text="Project IT PMe",
    )
    div_group = models.CharField(
        null=False,
        max_length=30,
        default="",
        help_text="Division Group",
    )
    # div_group = models.ForeignKey(
    #     ImpDiv,
    #     on_delete=models.CASCADE,
    #     help_text="Division ID",
    # )
    work_month = models.CharField(
        null=False,
        max_length=10,
        default="",
        help_text="Work Month on TSS",
    )
    work_hours = models.FloatField(
        null=False,
        help_text="Work Hour on TSS",
    )
    days = models.IntegerField(
        null=False,
        help_text="Work Days",
    )
    tss_mm = models.FloatField(
        null=False,
        help_text=" Man-Month on TSS",
    )

    class Meta:
        db_table = "imp_tsspast"
        unique_together = ("id", "pmcs_ib_project_year", "pmcs_ib_project_name", "ib_code", "div_group")
