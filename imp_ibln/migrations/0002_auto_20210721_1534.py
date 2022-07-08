# Generated by Django 3.2 on 2021-07-21 07:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imp_div', '0001_initial'),
        ('imp_ibln', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='impibln',
            old_name='ibid',
            new_name='ib',
        ),
        migrations.RenameField(
            model_name='impibln',
            old_name='divid',
            new_name='div',
        ),
        migrations.AlterUniqueTogether(
            name='impibln',
            unique_together={('id', 'project_year', 'project_name', 'div_group')},
        ),
    ]
