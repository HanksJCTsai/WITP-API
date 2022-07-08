from django.db import models

# Create your models here.
class ProjType(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    project_type = models.CharField(
        null=False,
        max_length=30,
        default="",
        help_text="Projectg Type",
    )

    class Meta:
        db_table = "imp_projtype"
        ordering = ['project_type']
