# Generated by Django 3.1.7 on 2022-03-03 09:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imp_div', '0006_alter_impdiv_options'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='impdiv',
            unique_together={('id', 'div', 'div_group')},
        ),
    ]
