# Generated by Django 3.2 on 2021-07-20 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imp_cal', '0003_alter_impcal_days'),
    ]

    operations = [
        migrations.AlterField(
            model_name='impcal',
            name='days',
            field=models.IntegerField(default='', help_text='Work Days'),
        ),
    ]
