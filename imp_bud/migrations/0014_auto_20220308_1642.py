# Generated by Django 3.2.12 on 2022-03-08 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imp_bud', '0013_merge_20220307_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='impbud',
            name='comments',
            field=models.CharField(blank=True, help_text='Project Comments', max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='impbud',
            name='recv_ep_code',
            field=models.CharField(blank=True, default='', help_text='EP Code', max_length=20),
        ),
    ]
