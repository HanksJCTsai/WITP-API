from django.db import models

# Create your models here.
class PmsJiraITUser (models.Model):
    class Meta:
        db_table = "pms_jira_it_user"
        ordering = ['jira_user_id']

    jira_user_id = models.CharField(
        max_length=100,
        primary_key=True,
        help_text="Jira User ID",
    )

    display_name = models.CharField(
        null=True,
        max_length=100,
        help_text="Jira User Name",
    )