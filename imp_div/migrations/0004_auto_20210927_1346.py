# Generated by Django 3.2.6 on 2021-09-27 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imp_div', '0003_rename_divcode_impdiv_div_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='impdiv',
            name='div_code',
        ),
        migrations.AddField(
            model_name='impdiv',
            name='div_group',
            field=models.CharField(default='', help_text='Division ID', max_length=10),
        ),
        migrations.AlterField(
            model_name='impdiv',
            name='div',
            field=models.CharField(default='', help_text='Division Code', max_length=20),
        ),
    ]
