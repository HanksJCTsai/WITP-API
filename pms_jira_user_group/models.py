from django.db import models

from pms_jira_user.models import PmsJiraUser

# Create your models here.
class PmsJiraUserGroup (models.Model):
    class Meta:
        db_table = "pms_jira_user_group"
        ordering = ['user_id', 'id']

    id = models.AutoField(
        primary_key=True,
    )
    user = models.ForeignKey(
        PmsJiraUser,
        related_name="pms_jira_user_group_user_id_fkey",
        on_delete=models.CASCADE,
        null=True,
    )
    jira_group = models.CharField(
        null=False,
        max_length=50,
        help_text="Jira Group",
    )
