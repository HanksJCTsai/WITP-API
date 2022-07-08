from imp_div.models import ImpDiv
from django.db import models

# Create your models here.
class ImpDept(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    dept = models.CharField(
        null=True,
        max_length=10,
        default="",
        help_text="Department ID",
    )
    div = models.ForeignKey(
        ImpDiv,
        on_delete=models.CASCADE,
        help_text="Division ID",
    )

    class Meta:
        db_table = "imp_dept"
        unique_together = ("id", "dept")
        ordering = ['dept', 'div']
