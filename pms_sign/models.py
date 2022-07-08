from django.db import models
from pms_project.models import PmsProject

# Create your models here.
class PmsSign (models.Model):
    class Meta:
        db_table = "pms_sign_head"

    id = models.AutoField(
        primary_key=True,
    )
    project = models.ForeignKey(
        PmsProject,
        related_name="pms_sign_head_project_id_fkey",
        on_delete=models.CASCADE,
        null=True,
    )
    sign_id = models.CharField(
        null=False,
        max_length=20,
        help_text="Sign ID", 
    )
    result = models.CharField(
        null=True,
        max_length=10,
        help_text="Result. APPROVED; REJECTED;",
    )
    requester_remark = models.TextField(
        null=True,
        help_text="Remark",
    )
    create_date = models.DateTimeField(
        null=False,
        auto_now_add=True,
        help_text="Created Date",
    )
    signed_date = models.DateTimeField(
        null=True,
        help_text="Signed Date",
    )
    mcp_id = models.IntegerField(
        null=True,
        help_text="MCP ID",
    )

class PmsSignContent (models.Model):
    class Meta:
        db_table = "pms_sign_content"
        
    sign = models.OneToOneField(
        PmsSign,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    project_content = models.JSONField(
        null=False,
        help_text="Project Content",
    )
    update_user = models.JSONField(
        null=False,
        help_text="Update User",
    )

class PmsSignDetail (models.Model):
    class Meta:
        db_table = "pms_sign_detail"

    id = models.AutoField(
        primary_key=True,
    )
    sign = models.ForeignKey(
        PmsSign,
        related_name="pms_sign_detail_pms_sign_head_id_fkey",
        on_delete=models.CASCADE,
        null=True,
    )
    seq = models.IntegerField(
        null=False,
        help_text="Sequence",
    )
    division = models.CharField(
        null=False,
        max_length=10,
        help_text="Division",
    )
    sign_user = models.CharField(
        null=False,
        max_length=50,
        help_text="Sign User",
    )
    sign_user_employee_id = models.CharField(
        null=True,
        max_length=20,
        help_text="Sign User Employee ID",
    )
    sign_user_email = models.TextField(
        null=False,
        help_text="Sign User EMail",
    )
    result = models.CharField(
        null=True,
        max_length=10,
        help_text="Result. APPROVED; REJECTED;",
    )
    remark = models.TextField(
        null=True,
        help_text="Remark",
    )
    signed_date = models.DateTimeField(
        null=True,
        help_text="Signed Date",
    )

class PmsSignId (models.Model):
    class Meta:
        db_table = "pms_sign_id"

    id = models.AutoField(
        primary_key=True,
    )
    sign_id = models.IntegerField(
        null=False,
        help_text="Max Sign ID", 
    )
    create_date = models.DateTimeField(
        null=False,
        auto_now_add=True,
        help_text="Created Date",
    )
