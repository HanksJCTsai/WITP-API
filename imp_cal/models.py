from django.db import models

# Create your models here.
class ImpCal(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    country = models.CharField(
        null=False,
        max_length=10,
        default="TW",
        help_text="Country Name",
    )
    year = models.CharField(
        null=False,
        max_length=4,
        default="",
        help_text="Year",
    )
    month = models.CharField(
        null=False,
        max_length=2,
        default="",
        help_text="Month",
    )
    days = models.IntegerField(
        null=False,
        default="",
        help_text="Work Days",
    )
    creater = models.CharField(
        null=True,
        blank=True,
        max_length=50,
        help_text="Cal Creater",
    )
    creatdate = models.DateTimeField(
        null=True,
    )
    updater = models.CharField(
        null=True,
        blank=True,
        max_length=50,
        help_text="Cal Updater",
    )
    updatedate = models.DateTimeField(
        null=True,
    )

    class Meta:
        db_table = "imp_cal"
        unique_together = ["id", "country", "year", "month"]
        ordering = ['year', 'month', 'days', 'country']
