# Generated by Django 3.2.12 on 2022-05-20 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pms_sign', '0006_alter_pmssign_mcp_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='pmssigndetail',
            name='sign_user_employee_id',
            field=models.CharField(help_text='Sign User Employee ID', max_length=20, null=True),
        ),
    ]
