# Generated by Django 3.2 on 2021-07-21 10:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imp_budln', '0002_auto_20210721_1534'),
    ]

    operations = [
        migrations.RenameField(
            model_name='impbudln',
            old_name='aprplan',
            new_name='apr_plan',
        ),
        migrations.RenameField(
            model_name='impbudln',
            old_name='augplan',
            new_name='aug_plan',
        ),
        migrations.RenameField(
            model_name='impbudln',
            old_name='decplan',
            new_name='dec_plan',
        ),
        migrations.RenameField(
            model_name='impbudln',
            old_name='febplan',
            new_name='feb_plan',
        ),
        migrations.RenameField(
            model_name='impbudln',
            old_name='janplan',
            new_name='jan_plan',
        ),
        migrations.RenameField(
            model_name='impbudln',
            old_name='julplan',
            new_name='jul_plan',
        ),
        migrations.RenameField(
            model_name='impbudln',
            old_name='marplan',
            new_name='mar_plan',
        ),
        migrations.RenameField(
            model_name='impbudln',
            old_name='mayplan',
            new_name='may_plan',
        ),
        migrations.RenameField(
            model_name='impbudln',
            old_name='novplan',
            new_name='nov_plan',
        ),
        migrations.RenameField(
            model_name='impbudln',
            old_name='octplan',
            new_name='oct_plan',
        ),
        migrations.RenameField(
            model_name='impbudln',
            old_name='projectname',
            new_name='project_name',
        ),
        migrations.RenameField(
            model_name='impbudln',
            old_name='projectyear',
            new_name='project_year',
        ),
        migrations.RenameField(
            model_name='impbudln',
            old_name='sepplan',
            new_name='sep_plan',
        ),
    ]
