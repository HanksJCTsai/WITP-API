from imp_bud.models import ImpBud
from django.db import models
from imp_bu.models import ImpBu
from imp_div.models import ImpDiv
from imp_resource.models import Resource

# Create your models here.
class ImpBudln(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    bud = models.ForeignKey(
        ImpBud,
        null=True,
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
    resource = models.CharField(
        null=False,
        max_length=30,
        default="",
        help_text="Team Name",
    )
    # resource = models.ForeignKey(
    #     Resource,
    #     on_delete=models.CASCADE,
    # )
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

    class Meta:
        db_table = "imp_budln"
        unique_together = ("resource", "project_year", "project_name")
        ordering = ['project_year', 'project_name', 'resource']
