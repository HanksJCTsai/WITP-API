# Generated by Django 3.2.6 on 2021-09-27 06:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imp_ib', '0003_auto_20210721_1819'),
    ]

    operations = [
        migrations.RenameField(
            model_name='impib',
            old_name='handle_div',
            new_name='handle_div_group',
        ),
    ]
