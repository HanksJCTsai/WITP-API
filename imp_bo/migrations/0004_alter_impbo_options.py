# Generated by Django 3.2.6 on 2021-10-15 01:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imp_bo', '0003_alter_impbo_bo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='impbo',
            options={'ordering': ['bo']},
        ),
    ]
