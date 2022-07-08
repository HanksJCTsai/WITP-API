from django.db import models

from pms_jira_user.models import PmsJiraUser

# Create your models here.
class PmsProject (models.Model):
    class Meta:
        db_table = "pms_prj_list"
        ordering = ['id']

    id = models.AutoField(
        primary_key=True,
    )
    project_name = models.CharField(
        null=False,
        max_length=50,
        help_text="Project Name",
    )
    division = models.CharField(
        null=False,
        max_length=10,
        help_text="Division",
    )
    division_supervisor = models.CharField(
        null=False,
        max_length=50,
        help_text="Division Supervison",
    )
    division_supervisor_email = models.TextField(
        null=False,
        help_text="Division Supervison EMail",
    )
    mode = models.CharField(
        null=False,
        max_length=10,
        help_text="Mode",
    )
    product_type = models.TextField(
        null=False,
        help_text="Product Type",
    )
    plan_start = models.DateField(
        null=False,
        help_text="Plan Start",
    )
    plan_end = models.DateField(
        null=False,
        help_text="Plan End",
    )
    jira_key = models.CharField(
        null=False,
        max_length=10,
        help_text="Jira Key",
    )
    jira_project_id = models.IntegerField(
        null=True,
        help_text="Jira Project ID",
    )
    jira_name = models.CharField(
        null=False,
        max_length=100,
        help_text="Jira Name",
    )
    user_contact = models.ForeignKey(
        PmsJiraUser,
        related_name="pms_prj_user_contact_user_id_fkey",
        on_delete=models.CASCADE,
        null=True,
    )
    # user_contact = models.CharField(
    #     null=False,
    #     max_length=50,
    #     help_text="User Contact",
    # )
    # user_contact_email = models.TextField(
    #     null=False,
    #     help_text="User Contact EMail",
    # )
    it_contact = models.ForeignKey(
        PmsJiraUser,
        related_name="pms_prj_it_contact_user_id_fkey",
        on_delete=models.CASCADE,
        null=True,
    )
    # it_contact = models.CharField(
    #     null=False,
    #     max_length=50,
    #     help_text="IT Contact",
    # )
    # it_contact_email = models.TextField(
    #     null=False,
    #     help_text="IT Contact EMail",
    # )
    status = models.IntegerField(
        null=False,
        default=0,
        help_text="Status",
    )
    involve_pms = models.BooleanField(
        null=False,
        default=True,
        help_text="Involve PMS"
    )
    involve_pms_start = models.DateField(
        null=True,
        help_text="Involve PMS Start Date",
    )
    involve_pms_end = models.DateField(
        null=True,
        help_text="Involve PMS End Date",
    )
    create_date = models.DateTimeField(
        null=False,
        auto_now_add=True,
        help_text="Create Date",
    )
    create_user = models.CharField(
        null=False,
        max_length=50,
        default="",
        help_text="Create User",
    )
    close = models.BooleanField(
        null=False,
        default=False,
        help_text="Close"
    )
    close_date = models.DateTimeField(
        null=True,
        help_text="Close Date",
    )
    approve_date = models.DateTimeField(
        null=True,
        help_text="Approve Date",
    )
    project_code = models.CharField(
        null=False,
        max_length=12,
        default="",
        help_text="Project Code",
    )
    confluence = models.BooleanField(
        null=False,
        default=False,
        help_text="Need To Create Confluence"
    )
    confluence_key = models.CharField(
        null=True,
        max_length=10,
        help_text="Confluence Key",
    )
    confluence_name = models.CharField(
        null=True,
        max_length=100,
        help_text="Confluence Name",
    )
    mvp_date = models.DateField(
        null=True,
        help_text="MVP Date",
    )  

class PmsProjectLog (models.Model):
    class Meta:
        db_table = "pms_prj_list_log"
        ordering = ['project_name']

    id = models.AutoField(
        primary_key=True,
    )
    project_id = models.IntegerField(
        null=False,
        default=0,
        help_text="Project ID",
    )
    project_name = models.CharField(
        null=False,
        max_length=50,
        help_text="Project Name",
    )
    division = models.CharField(
        null=False,
        max_length=10,
        help_text="Division",
    )
    division_supervisor = models.CharField(
        null=False,
        max_length=50,
        help_text="Division Supervison",
    )
    division_supervisor_email = models.TextField(
        null=False,
        help_text="Division Supervison EMail",
    )
    mode = models.CharField(
        null=False,
        max_length=10,
        help_text="Mode",
    )
    product_type = models.TextField(
        null=False,
        help_text="Product Type",
    )
    plan_start = models.DateField(
        null=False,
        help_text="Plan Start",
    )
    plan_end = models.DateField(
        null=False,
        help_text="Plan End",
    )
    jira_key = models.CharField(
        null=False,
        max_length=10,
        help_text="Jira Key",
    )
    jira_name = models.CharField(
        null=False,
        max_length=100,
        help_text="Jira Name",
    )
    user_contact = models.CharField(
        null=False,
        max_length=50,
        help_text="User Contact",
    )
    user_contact_email = models.TextField(
        null=False,
        help_text="User Contact EMail",
    )
    it_contact = models.CharField(
        null=False,
        max_length=50,
        help_text="IT Contact",
    )
    it_contact_email = models.TextField(
        null=False,
        help_text="IT Contact EMail",
    )
    status = models.IntegerField(
        null=False,
        default=0,
        help_text="Status",
    )
    involve_pms = models.BooleanField(
        null=False,
        default=True,
        help_text="Involve PMS"
    )
    involve_pms_start = models.DateField(
        null=True,
        help_text="Involve PMS Start Date",
    )
    involve_pms_end = models.DateField(
        null=True,
        help_text="Involve PMS End Date",
    )
    create_date = models.DateTimeField(
        null=False,
        help_text="Create Date",
    )
    create_user = models.CharField(
        null=False,
        max_length=50,
        default="",
        help_text="Create User",
    )
    close = models.BooleanField(
        null=False,
        default=False,
        help_text="Close"
    )
    close_date = models.DateTimeField(
        null=True,
        help_text="Close Date",
    )
    approve_date = models.DateTimeField(
        null=True,
        help_text="Approve Date",
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
    project_code = models.CharField(
        null=False,
        max_length=12,
        default="",
        help_text="Project Code",
    )
    confluence = models.BooleanField(
        null=False,
        default=False,
        help_text="Need To Create Confluence"
    )
    confluence_key = models.CharField(
        null=True,
        max_length=10,
        help_text="Confluence Key",
    )
    confluence_name = models.CharField(
        null=True,
        max_length=100,
        help_text="Confluence Name",
    )
    mvp_date = models.DateField(
        null=True,
        help_text="MVP Date",
    )  