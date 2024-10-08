# Generated by Django 3.2 on 2021-07-21 10:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imp_ib', '0002_rename_handledivid_impib_handlediv'),
    ]

    operations = [
        migrations.RenameField(
            model_name='impib',
            old_name='epcode',
            new_name='ep_code',
        ),
        migrations.RenameField(
            model_name='impib',
            old_name='handlediv',
            new_name='handle_div',
        ),
        migrations.RenameField(
            model_name='impib',
            old_name='ibcode',
            new_name='ib_code',
        ),
        migrations.RenameField(
            model_name='impib',
            old_name='itpm',
            new_name='it_pm',
        ),
        migrations.RenameField(
            model_name='impib',
            old_name='monthlypajdone',
            new_name='monthly_paj_done',
        ),
        migrations.RenameField(
            model_name='impib',
            old_name='planfinish',
            new_name='plan_finish',
        ),
        migrations.RenameField(
            model_name='impib',
            old_name='planstart',
            new_name='plan_start',
        ),
        migrations.RenameField(
            model_name='impib',
            old_name='pmcsepprojectname',
            new_name='pmcs_ep_project_name',
        ),
        migrations.RenameField(
            model_name='impib',
            old_name='pmcsibprojectname',
            new_name='pmcs_ib_project_name',
        ),
        migrations.RenameField(
            model_name='impib',
            old_name='projectname',
            new_name='project_name',
        ),
        migrations.RenameField(
            model_name='impib',
            old_name='projectyear',
            new_name='project_year',
        ),
        migrations.AlterUniqueTogether(
            name='impib',
            unique_together={('id', 'project_year', 'project_name', 'ib_code', 'ep_code')},
        ),
    ]
