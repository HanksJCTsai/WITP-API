# Generated by Django 3.1.7 on 2022-03-07 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imp_tss', '0012_merge_20220305_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imptss',
            name='ib_code',
            field=models.CharField(default='', help_text='IB Code', max_length=20),
        ),
    ]
