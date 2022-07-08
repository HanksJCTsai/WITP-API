from django.db import models

# Create your models here.
class PmsJiraProjectRole (models.Model):
    class Meta:
        db_table = "pms_jira_project_role"
        ordering = ['jira_project_id', 'project_role', 'id']

    id = models.AutoField(
        primary_key=True,
    )
    jira_key = models.CharField(
        null=False,
        max_length=20,
        help_text="Jira Key",
    )
    jira_project_id = models.IntegerField(
        null=True,
        help_text="Jira Project ID",
    )
    project_role = models.CharField(
        null=False,
        max_length=50,
        help_text="Project Role",
    )
    jira_user_id = models.CharField(
        null=True,
        max_length=100,
        help_text="Jira User ID",
    )