# Generated by Django 3.2.12 on 2022-05-18 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pms_sign', '0003_pmssigncontent'),
    ]

    operations = [
        migrations.AddField(
            model_name='pmssign',
            name='mcp_id',
            field=models.IntegerField(help_text='MCP ID', null=True),
        ),
    ]
