from django.db import models
from imp_div.models import ImpDiv
from imp_prf.models import ImpPrf

# Create your models here.
class ImpPrfln(models.Model):
    id = models.AutoField(
        primary_key=True,
    )

    prf = models.ForeignKey(
        ImpPrf,
        on_delete=models.CASCADE,
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

    div_group = models.CharField(
        null=False,
        max_length=30,
        default="",
        help_text="Division Group",
    )

    jan_plan = models.FloatField(
        help_text="Plan HC on Jan",
    )

    feb_plan = models.FloatField(
        help_text="Plan HC on feb",
    )

    mar_plan = models.FloatField(
        help_text="Plan HC on mar",
    )

    apr_plan = models.FloatField(
        help_text="Plan HC on apr",
    )

    may_plan = models.FloatField(
        help_text="Plan HC on may",
    )

    jun_plan = models.FloatField(
        help_text="Plan HC on June",
    )

    jul_plan = models.FloatField(
        help_text="Plan HC on July",
    )

    aug_plan = models.FloatField(
        help_text="Plan HC on aug",
    )

    sep_plan = models.FloatField(
        help_text="Plan HC on sep",
    )

    oct_plan = models.FloatField(
        help_text="Plan HC on oct",
    )

    nov_plan = models.FloatField(
        help_text="Plan HC on nov",
    )

    dec_plan = models.FloatField(
        help_text="Plan HC on dec",
    )

    creater = models.CharField(
        null=True,
        blank=True,
        max_length=50,
        default="",
        help_text="PRFLN Creater",
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
        help_text="PRFLN Updater",
    )

    updatedate = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "imp_prfln"
        unique_together = ("id", "project_year", "project_name", "div_group")
