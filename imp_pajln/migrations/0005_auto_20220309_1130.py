# Generated by Django 3.2.12 on 2022-03-09 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imp_pajln', '0004_rename_div_pajln_div_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='pajln',
            name='project_name',
            field=models.CharField(default='', help_text='Project Name', max_length=100),
        ),
        migrations.AddField(
            model_name='pajln',
            name='project_year',
            field=models.CharField(default='', help_text='Project Year', max_length=4),
        ),
        migrations.AlterField(
            model_name='pajln',
            name='div_group',
            field=models.CharField(default='', help_text='Division Group', max_length=30),
        ),
        migrations.AlterField(
            model_name='pajln',
            name='ib_code',
            field=models.CharField(default='', help_text='IB code', max_length=20),
        ),
        migrations.AlterUniqueTogether(
            name='pajln',
            unique_together={('id', 'project_year', 'project_name', 'ib_code', 'div_group')},
        ),
        migrations.RemoveField(
            model_name='pajln',
            name='paj_year',
        ),
    ]
