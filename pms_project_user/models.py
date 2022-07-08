from django.db import models
from pms_project.models import PmsProject
from pms_jira_user.models import PmsJiraUser
from pms_sign.models import PmsSign

# Create your models here.
class PmsProjectUser (models.Model):
    class Meta:
        db_table = "pms_prj_user"
        ordering = ['project_id', 'id']        
        unique_together = ('project_id', 'user_id', 'deleted')

    id = models.AutoField(
        primary_key=True,
    )
    user = models.ForeignKey(
        PmsJiraUser,
        related_name="pms_prj_user_user_id_fkey",
        on_delete=models.CASCADE,
        null=True,
    )
    project = models.ForeignKey(
        PmsProject,
        related_name="pms_prj_user_project_id_fkey",
        on_delete=models.CASCADE,
        null=True,
    )
    project_role = models.CharField(
        null=False,
        max_length=20,
        help_text="Project Role",
    )
    jira_role = models.CharField(
        null=False,
        max_length=15,
        help_text="Jira Role",
    )
    join_date = models.DateTimeField(
        null=False,
        auto_now_add=True,
        help_text="Join Date",
    )
    deleted = models.BooleanField(
        null=False,
        default=False,
        help_text="Wait for Delete from Project"
    )

class PmsProjectUserLog (models.Model):
    class Meta:
        db_table = "pms_prj_user_log"
        ordering = ['project_id', 'id']        

    id = models.AutoField(
        primary_key=True,
    )
    project_user_id = models.IntegerField(
        null=False,
        default=0,
        help_text="Project User ID",
    )
    user_id = models.IntegerField(
        null=False,
        default=0,
        help_text="User ID",
    )
    project_id = models.IntegerField(
        null=False,
        default=0,
        help_text="Project ID",
    )
    project_role = models.CharField(
        null=False,
        max_length=20,
        help_text="Project Role",
    )
    jira_role = models.CharField(
        null=False,
        max_length=15,
        help_text="Jira Role",
    )
    join_date = models.DateTimeField(
        null=False,
        auto_now_add=True,
        help_text="Join Date",
    )
    action = models.CharField(
        null=False,
        max_length=10,
        help_text="Action",
    )
    trn_date = models.DateTimeField(
        null=False,
        auto_now_add=True,
        help_text="Tansaction Date",
    )
    trn_user = models.CharField(
        null=False,
        max_length=50,
        help_text="Tansaction User",
    )
    approved = models.BooleanField(
        null=False,
        default=False,
        help_text="Approved",
    )
    user_name = models.CharField(
        null=False,
        max_length=50,
        default='',
        help_text="User Name",
    )
    employee_id = models.CharField(
        null=True,
        max_length=20,
        help_text="Employee ID",
    )
    email = models.TextField(
        null=False,
        help_text="E-Mail",
        default='',
    )
