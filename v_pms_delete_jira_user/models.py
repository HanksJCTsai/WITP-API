from django.db import models

# Create your models here.
class VPmsDeleteJiraUser (models.Model):
    class Meta:
        db_table = "v_pms_delete_jira_user"
        ordering = ['id']
        managed = False

    id = models.IntegerField(
        primary_key=True,
        null=False,
        help_text="User ID",
    )
    user_name = models.CharField(
        null=False,
        max_length=50,
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
        unique=True,
    )
    status = models.IntegerField(
        null=False,
        default=1,
        help_text="Status",
    )
    create_date = models.DateTimeField(
        null=False,
        auto_now_add=True,
        help_text="Create Date",
    )
    deleted_date = models.DateTimeField(
        null=True,
        help_text="Deleted Date",
    )
    org_role = models.CharField(
        null=True,
        max_length=10,
        help_text="Organization Role",
    )
    jira_user_id = models.CharField(
        null=True,
        max_length=100,
        help_text="Jira User ID",
    )
    add_to_org_date = models.DateTimeField(
        null=True,
        auto_now_add=True,
        help_text="Add into Org Date",
    )
    last_seen_in_jira = models.DateTimeField(
        null=True,
        help_text="Last Seen In Jira Date",
    )