from django.db import models
from imp_bo.models import ImpBo

# Create your models here.
class ImpBg(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    bg = models.CharField(
        max_length=20,
        default="",
        help_text="BG Names",
    )
    bo = models.ForeignKey(
        ImpBo,
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "imp_bg"
        ordering = ['bg', 'bo']
