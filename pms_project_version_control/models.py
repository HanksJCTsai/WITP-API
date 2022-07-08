from django.db import models
from pms_project.models import PmsProject

# Create your models here.
class PmsProjectVersionControl (models.Model):
    class Meta:
        db_table = "pms_prj_version_control"
        ordering = ['project_id', 'id']
        unique_together = ('project_id', 'type', 'repo_id')

    id = models.AutoField(
        primary_key=True,
    )
    project = models.ForeignKey(
        PmsProject,
        related_name="pms_prj_version_control_project_id_fkey",
        on_delete=models.CASCADE,
        null=True,
    )
    version_control = models.CharField(
        null=False,
        max_length=10,
        help_text="Version Control",
    )
    type = models.CharField(
        null=False,
        max_length=10,
        help_text="type",
    )
    repo_id = models.IntegerField(
        null=False,
        help_text="Repository ID",
    )
    ut_job_name = models.CharField(
        null=True,
        max_length=20,
        help_text="UT Job Name",
    )
    repo_url = models.TextField(
        null=True,
        help_text="UT Url",
    )
