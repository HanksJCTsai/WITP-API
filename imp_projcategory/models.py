from django.db import models

# Create your models here.
class ProjCategory(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    project_category = models.CharField(
        null=False,
        max_length=30,
        default="",
        help_text="Projectg Category",
    )

    class Meta:
        db_table = "imp_projcategory"
        ordering = ["project_category"]
