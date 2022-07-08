from django.db import models
from imp_div.models import ImpDiv

# Create your models here.
class Resource(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    resource_group = models.CharField(
        null=False,
        max_length=30,
        default="",
        help_text="Team Name",
    )
    location = models.CharField(
        null=False,
        max_length=30,
        default="",
        help_text="location",
    )
    system = models.CharField(
        null=False,
        max_length=30,
        default="",
        help_text="",
    )
    division = models.CharField(
        null=False,
        max_length=30,
        default="",
        help_text="",
    )
    div_group = models.ForeignKey(
        ImpDiv, on_delete=models.CASCADE, help_text="Division ID", null=True
    )
    remark = models.CharField(
        null=True,
        blank = True,
        max_length=100,
        default="",
        help_text="",
    )

    class Meta:
        db_table = "imp_resource"
        ordering = ['resource_group', 'div_group', 'division', 'location', 'system']
