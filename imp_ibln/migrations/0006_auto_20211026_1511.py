# Generated by Django 3.1.7 on 2021-10-26 07:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imp_div', '0006_alter_impdiv_options'),
        ('imp_ibln', '0005_impibln_ib'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='impibln',
            unique_together={('id', 'project_year', 'project_name', 'div_group')},
        )
    ]
