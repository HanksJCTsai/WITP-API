from django.db import models
from imp_dept.models import ImpDept

# Create your models here.
class ImpTss(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    employee_id = models.CharField(
        null=False,
        max_length=50,
        default="",
        help_text="Wistron Employee ID",
    )
    employee_name = models.CharField(
        null=False,
        max_length=50,
        default="",
        help_text="Wistron Employee Name",
    )
    department = models.CharField(
        null=False,
        max_length=10,
        default="",
        help_text="Wistron Department ID",
    )
    ib_code = models.CharField(
        null=False,
        max_length=20,
        default="",
        help_text="IB Code",
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
    project_leader = models.CharField(
        null=False, max_length=50, default="", help_text="Wistron Project Leader"
    )
    task_category = models.CharField(
        null=False,
        max_length=50,
        default="",
        help_text="Task Category on TSS",
    )
    task_item = models.CharField(
        null=False,
        max_length=100,
        default="",
        help_text="Task Item on TSS",
    )
    date = models.DateField(
        null=False,
        default="",
    )
    working_hour = models.FloatField(
        null=False,
        help_text="Working Hour on TSS",
    )
    description = models.CharField(
        null=False,
        max_length=2000,
        default="",
        help_text="Description",
    )
    tag = models.CharField(
        null=False,
        max_length=100,
        default="",
        help_text="Tag on TSS",
    )
    profit_center_models = models.CharField(
        null=False,
        max_length=100,
        default="",
        help_text="Task Item on TSS",
    )
    profit_center = models.CharField(
        null=True,
        max_length=100,
        default="",
        help_text="Profit Center",
    )
    # charge_dept = models.ForeignKey(
    #     ImpDept,
    #     on_delete=models.CASCADE,
    #     help_text="Charge Department ID",
    # )

    charge_dept = models.CharField(
        null=False,
        max_length=10,
        default="",
        help_text="Charge Department",
    )

    seq = models.DateTimeField(
        null=False,
        help_text="Seq DataTime",
    )

    pmcs_ib_project_year = models.CharField(
        null=False,
        max_length=4,
        default="",
        help_text="IB Project Year"
    )

    class Meta:
        db_table = "imp_tss"
        unique_together = (
            "id",
            "employee_id",
            "ib_code",
            "task_category",
            "task_item",
            "date",
            "tag",
        )
