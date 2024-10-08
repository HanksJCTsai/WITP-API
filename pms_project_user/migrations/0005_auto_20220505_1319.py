# Generated by Django 3.2.12 on 2022-05-05 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pms_project_user', '0004_pmsprojectuserlog_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='pmsprojectuserlog',
            name='email',
            field=models.TextField(default='', help_text='E-Mail'),
        ),
        migrations.AddField(
            model_name='pmsprojectuserlog',
            name='employee_id',
            field=models.CharField(help_text='Employee ID', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='pmsprojectuserlog',
            name='user_name',
            field=models.CharField(default='', help_text='User Name', max_length=50),
        ),
    ]
