from django.db import models

# Create your models here.
class VPmsUserInJira (models.Model):
    class Meta:
        db_table = "v_pms_user_in_jira"
        managed = False

    jira_key = models.CharField(
        max_length=20,
        help_text="Project Jira Key",
    )
    jira_project_id = models.IntegerField(
        help_text="Project Jira ID",
    )
    jira_user_id = models.CharField(
        null=False,
        max_length=100,
        help_text="User Jira ID",
    )
    display_name = models.CharField(
        null=False,
        max_length=100,
        help_text="User Jira Name",
    )
    pms_jira_user_id = models.CharField(
        max_length=100,
        help_text="User Jira ID in PMS",
    )
    project_role = models.CharField(
        max_length=50,
        help_text="Project Role",
    )
    pms_project_id = models.IntegerField(
        help_text="Project Jira ID in PMS",
    )
    pms_user_id = models.IntegerField(
        help_text="PMS User ID",
    )
    division = models.CharField(
        max_length=10,
        help_text="Division",
    )
    project_name = models.CharField(
        max_length=50,
        help_text="Project Name",
    )
    jira_name = models.CharField(
        max_length=100,
        help_text="Jira Project Name",
    )