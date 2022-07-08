from django.db import models
from imp_div.models import ImpDiv

# Create your models here.
class Pajln(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    ib_code = models.CharField(
        null=False,
        max_length=20,
        default="",
        help_text="IB code",
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
    project_year = models.CharField(
        null=False,
        max_length=4,
        default="",
        help_text="Project Year",
    )
    # paj_year = models.CharField(
    #     null=False,
    #     max_length=4,
    #     default="",
    #     help_text="PAJ Year",
    # )
    project_name = models.CharField(
        null=False,
        max_length=100,
        default="",
        help_text="Project Name",
    )
    jan_plan = models.FloatField(
        help_text="Plan HC on Jan",
    )
    jan_paj_no = models.CharField(
        blank=True,
        null=True,
        max_length=20,
        default="",
        help_text="PAJ number for Jan",
    )
    feb_plan = models.FloatField(
        help_text="Plan HC on feb",
    )
    feb_paj_no = models.CharField(
        blank=True,
        null=True,
        max_length=20,
        default="",
        help_text="PAJ number for Fab"
    )
    mar_plan = models.FloatField(
        help_text="Plan HC on mar",
    )
    mar_paj_no = models.CharField(
        blank=True,
        null=True,
        max_length=20,
        default="",
        help_text="PAJ number for Mar"
    )
    apr_plan = models.FloatField(
        help_text="Plan HC on apr",
    )
    apr_paj_no = models.CharField(
        blank=True,
        null=True,
        max_length=20,
        default="",
        help_text="PAJ number for Apr"
    )
    may_plan = models.FloatField(
        help_text="Plan HC on may",
    )
    may_paj_no = models.CharField(
        blank=True,
        null=True,
        max_length=20,
        default="",
        help_text="PAJ number for May"
    )
    jun_plan = models.FloatField(
        help_text="Plan HC on June",
    )
    jun_paj_no = models.CharField(
        blank=True,
        null=True,
        max_length=20,
        default="",
        help_text="PAJ number for Jun"
    )
    jul_plan = models.FloatField(
        help_text="Plan HC on July",
    )
    jul_paj_no = models.CharField(
        blank=True,
        null=True,
        max_length=20,
        default="",
        help_text="PAJ number for Jul"
    )
    aug_plan = models.FloatField(
        help_text="Plan HC on aug",
    )
    aug_paj_no = models.CharField(
        blank=True,
        null=True,
        max_length=20,
        default="",
        help_text="PAJ number for Aug"
    )
    sep_plan = models.FloatField(
        help_text="Plan HC on sep",
    )
    sep_paj_no = models.CharField(
        blank=True,
        null=True,
        max_length=20,
        default="",
        help_text="PAJ number for Sep"
    )
    oct_plan = models.FloatField(
        help_text="Plan HC on oct",
    )
    oct_paj_no = models.CharField(
        blank=True,
        null=True,
        max_length=20,
        default="",
        help_text="PAJ number for Oct"
    )
    nov_plan = models.FloatField(
        help_text="Plan HC on nov",
    )
    nov_paj_no = models.CharField(
        blank=True,
        null=True,
        max_length=20,
        default="",
        help_text="PAJ number for Nov"
    )
    dec_plan = models.FloatField(
        help_text="Plan HC on dec",
    )
    dec_paj_no = models.CharField(
        blank=True,
        null=True,
        max_length=20,
        default="",
        help_text="PAJ number for Dec"
    )
    creater = models.CharField(
        null=True,
        blank=True,
        max_length=50,
        default="",
        help_text="PAJLN Creater",
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
        help_text="PAJLN Updater",
    )
    updatedate = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "imp_pajln"
        unique_together = ("id","project_year","project_name","ib_code","div_group")
