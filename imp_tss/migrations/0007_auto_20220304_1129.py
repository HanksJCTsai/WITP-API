# Generated by Django 3.1.7 on 2022-03-04 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imp_tss', '0006_alter_imptss_unique_together'),
    ]

    operations = [
        # migrations.AddField(
        #     model_name='imptss',
        #     name='pmcs_ib_project_year',
        #     field=models.CharField(default='', help_text='IB Project Year', max_length=4),
        # ),
        migrations.AlterField(
            model_name='imptss',
            name='charge_dept',
            field=models.CharField(default='', help_text='Charge Department', max_length=10),
        ),
        migrations.AlterField(
            model_name='imptss',
            name='description',
            field=models.CharField(default='', help_text='Description', max_length=2000),
        ),
        migrations.AlterField(
            model_name='imptss',
            name='employee_id',
            field=models.CharField(default='', help_text='Wistron Employee ID', max_length=50),
        ),
    ]
