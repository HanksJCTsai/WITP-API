# Generated by Django 3.2 on 2021-07-21 07:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imp_bud', '0002_alter_impbud_recvepcode'),
    ]

    operations = [
        migrations.RenameField(
            model_name='impbud',
            old_name='buid',
            new_name='bu',
        ),
    ]
