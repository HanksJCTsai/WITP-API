from django.db import models

# Create your models here.
class PajMonth(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    ref = models.CharField(
        null=False,
        max_length=1,
        default="",
        help_text="Ref",
    )
    project_year = models.CharField(
        null=False,
        max_length=4,
        default="",
        help_text="Project Year",
    )
    project_month = models.CharField(
        null=False,
        max_length=5,
        default="",
        help_text="Project Month",
    )

    class Meta:
        db_table = "imp_pajmonth"
