# Generated by Django 3.2.6 on 2021-09-27 06:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imp_tsspast', '0004_auto_20210721_1819'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imptsspast',
            old_name='div',
            new_name='div_group',
        ),
    ]
