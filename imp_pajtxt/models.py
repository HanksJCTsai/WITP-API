from django.db import models


# Create your models here.
class PajTxt(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    issue_dept = models.CharField(
        null=False,
        max_length=100,
        default="",
        help_text="Issue Dept",
    )
    issue_code = models.CharField(
        null=False,
        max_length=100,
        default="",
        help_text="Issue Code",
    )
    currency = models.CharField(
        null=False,
        max_length=100,
        default="",
    )
    reviewer1 = models.CharField(
        null=False,
        max_length=100,
        default="",
    )
    reviewer2 = models.CharField(
        null=False,
        max_length=100,
        default="",
    )
    charge_type = models.CharField(
        null=False,
        max_length=100,
        default="",
    )
    short_remark = models.CharField(
        null=False,
        max_length=100,
        default="",
    )
    remark = models.CharField(
        null=False,
        max_length=100,
        default="",
    )
    sbg_charge_type = models.CharField(
        null=False,
        max_length=100,
        default="",
        help_text="SBG Charge Type",
    )
    recv_dept = models.CharField(
        null=False,
        max_length=100,
        default="",
    )
    recv_pcode = models.CharField(
        null=False,
        max_length=100,
        default="",
    )
    amount = models.CharField(
        null=False,
        max_length=100,
        default="",
    )
    item_text = models.CharField(
        null=False,
        max_length=100,
        default="",
    )
    assignment = models.CharField(
        null=False,
        max_length=100,
        default="",
    )
    business_type = models.CharField(
        null=False,
        max_length=100,
        default="",
    )
    customer_name = models.CharField(
        null=False,
        max_length=100,
        default="",
    )
    reason = models.CharField(
        null=False,
        max_length=100,
        default="",
        help_text="Reason",
    )

    class Meta:
        db_table = "imp_pajtxt"
