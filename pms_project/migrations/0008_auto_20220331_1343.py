# Generated by Django 3.2.12 on 2022-03-31 05:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pms_jira_user', '0006_delete_pmsjirausergroup'),
        ('pms_project', '0007_auto_20220224_1025'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pmsproject',
            name='it_contact_email',
        ),
        migrations.RemoveField(
            model_name='pmsproject',
            name='user_contact_email',
        ),
        migrations.AlterField(
            model_name='pmsproject',
            name='it_contact',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pms_prj_it_contact_user_id_fkey', to='pms_jira_user.pmsjirauser'),
        ),
        migrations.AlterField(
            model_name='pmsproject',
            name='user_contact',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pms_prj_user_contact_user_id_fkey', to='pms_jira_user.pmsjirauser'),
        ),
    ]
