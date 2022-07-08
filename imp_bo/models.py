from django.db import models

# Create your models here.
class ImpBo(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    bo = models.CharField(
        max_length=20,
        default="",
        help_text="BO Names",
    )

    class Meta:
        db_table = "imp_bo"
        ordering = ['bo']
