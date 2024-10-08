# Generated by Django 3.2.12 on 2022-03-23 01:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imp_cal', '0008_auto_20220322_1119'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='impcal',
            options={'ordering': ['year', 'month', 'days', 'country']},
        ),
        migrations.RenameField(
            model_name='impcal',
            old_name='countury',
            new_name='country',
        ),
        migrations.AlterUniqueTogether(
            name='impcal',
            unique_together={('id', 'country', 'year', 'month')},
        ),
    ]
