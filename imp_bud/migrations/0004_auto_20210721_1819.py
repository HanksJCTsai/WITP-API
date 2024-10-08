# Generated by Django 3.2 on 2021-07-21 10:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imp_bud', '0003_rename_buid_impbud_bu'),
    ]

    operations = [
        migrations.RenameField(
            model_name='impbud',
            old_name='bizowner',
            new_name='biz_owner',
        ),
        migrations.RenameField(
            model_name='impbud',
            old_name='budsystrecvchgdeptid',
            new_name='bud_syst_recv_chg_dept',
        ),
        migrations.RenameField(
            model_name='impbud',
            old_name='contactwindow',
            new_name='contact_window',
        ),
        migrations.RenameField(
            model_name='impbud',
            old_name='handledivid',
            new_name='handle_div',
        ),
        migrations.RenameField(
            model_name='impbud',
            old_name='itpm',
            new_name='it_pm',
        ),
        migrations.RenameField(
            model_name='impbud',
            old_name='planfinish',
            new_name='plan_finish',
        ),
        migrations.RenameField(
            model_name='impbud',
            old_name='planstart',
            new_name='plan_start',
        ),
        migrations.RenameField(
            model_name='impbud',
            old_name='projectcategoryid',
            new_name='project_category',
        ),
        migrations.RenameField(
            model_name='impbud',
            old_name='projectname',
            new_name='project_name',
        ),
        migrations.RenameField(
            model_name='impbud',
            old_name='projecttypeid',
            new_name='project_type',
        ),
        migrations.RenameField(
            model_name='impbud',
            old_name='projectyear',
            new_name='project_year',
        ),
        migrations.RenameField(
            model_name='impbud',
            old_name='recvchgdeptid',
            new_name='recv_chg_dept',
        ),
        migrations.RenameField(
            model_name='impbud',
            old_name='recvepcode',
            new_name='recv_ep_code',
        ),
        migrations.AlterUniqueTogether(
            name='impbud',
            unique_together={('id', 'project_year', 'project_name', 'recv_ep_code')},
        ),
    ]
