from django.db import models
from imp_bo.models import ImpBo
from imp_bg.models import ImpBg

# Create your models here.
class ImpBu(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    bu = models.CharField(
        max_length=20,
        default="",
        help_text="BU Names",
    )
    bg = models.ForeignKey(
        ImpBg,
        on_delete=models.CASCADE,
    )
    bo = models.ForeignKey(
        ImpBo,
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "imp_bu"
        ordering = ['bu', 'bg', 'bo']
