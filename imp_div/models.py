from django.db import models

# Create your models here.
class ImpDiv(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    div_group = models.CharField(
        null=False,
        max_length=10,
        default="",
        help_text="Division ID",
    )
    functions = models.CharField(
        null=False,
        max_length=50,
        default="",
        help_text="Funtion",
    )
    div = models.CharField(
        null=False,
        max_length=20,
        default="",
        help_text="Division Code",
    )
    rate = models.IntegerField(
        null=False,
        default="",
        help_text="HC Rate",
    )

    class Meta:
        db_table = "imp_div"
        unique_together = ("id", "div", "div_group")
        ordering = ['div', 'div_group', 'functions', 'rate']
