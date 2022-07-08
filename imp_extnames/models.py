from django.db import models
from imp_div.models import ImpDiv

# Create your models here.
class extnames(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    emp_name = models.CharField(
        null=False,
        max_length=50,
        default="",
        help_text="Employee Names",
    )
    div_group = models.ForeignKey(
        ImpDiv,
        on_delete=models.CASCADE,
        help_text="Division ID",
    )

    class Meta:
        db_table = "imp_extnames"
        ordering = ['emp_name', 'div_group']
