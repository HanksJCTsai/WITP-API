# Generated by Django 3.1.7 on 2022-03-02 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imp_tss', '0008_auto_20220302_1007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imptss',
            name='employee_id',
            field=models.CharField(default='', help_text='Wistron Employee ID', max_length=50),
        ),
    ]
