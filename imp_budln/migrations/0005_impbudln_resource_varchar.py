# Generated by Django 3.2 on 2021-07-27 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("imp_budln", "0004_rename_junplan_impbudln_jun_plan"),
    ]

    operations = [
        migrations.AddField(
            model_name="impbudln",
            name="resource_varchar",
            field=models.CharField(max_length=10, null=True),
        ),
    ]
