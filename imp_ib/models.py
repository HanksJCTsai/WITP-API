from django.db import models

# Create your models here.
class ImpIb(models.Model):
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
        max_length=50,
        default="",
        help_text="Project IT PM",
    )
    plan_start = models.DateField(
        null=True,
    )
    plan_finish = models.DateField(
        null=True,
    )
    ib_code = models.CharField(
        null=False,
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
    ep_code = models.CharField(
        null=False,
        max_length=20,
        default="",
        help_text="EP Code",
    )
    pmcs_ep_project_name = models.CharField(
        null=False,
        max_length=100,
        default="",
        help_text="EP Project Name",
    )
    handle_div = models.CharField(
        null=False,
        max_length=20,
        default="",
        help_text="Division Code",
    )
    # handle_div_group = models.ForeignKey(
    #     ImpDiv,
    #     on_delete=models.CASCADE,
    # )
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
    monthly_paj_done = models.CharField(
        max_length=1,
        default="N",
        help_text="PAJ done by Monthly",
    )
    creater = models.CharField(
        null=True,
        blank=True,
        max_length=50,
        help_text="IB Creater",
    )
    creatdate = models.DateTimeField(
        null=True,
    )
    updater = models.CharField(
        null=True,
        blank=True,
        max_length=50,
        help_text="IB Updater",
    )
    updatedate = models.DateTimeField(
        null=True,
    )

    class Meta:
        db_table = "imp_ib"
        unique_together = ("id", "project_year", "project_name", "ib_code", "ep_code")
        ordering = ['project_year', 'project_name', 'complete', 'cancelled']
