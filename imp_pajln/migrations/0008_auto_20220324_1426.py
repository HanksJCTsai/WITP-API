# Generated by Django 3.2.12 on 2022-03-24 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imp_pajln', '0007_auto_20220322_1724'),
    ]

    operations = [
        migrations.AddField(
            model_name='pajln',
            name='apr_paj_no',
            field=models.CharField(blank=True, default='', help_text='PAJ number for Apr', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='pajln',
            name='aug_paj_no',
            field=models.CharField(blank=True, default='', help_text='PAJ number for Aug', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='pajln',
            name='dec_paj_no',
            field=models.CharField(blank=True, default='', help_text='PAJ number for Dec', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='pajln',
            name='feb_paj_no',
            field=models.CharField(blank=True, default='', help_text='PAJ number for Fab', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='pajln',
            name='jan_paj_no',
            field=models.CharField(blank=True, default='', help_text='PAJ number for Jan', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='pajln',
            name='jul_paj_no',
            field=models.CharField(blank=True, default='', help_text='PAJ number for Jul', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='pajln',
            name='jun_paj_no',
            field=models.CharField(blank=True, default='', help_text='PAJ number for Jun', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='pajln',
            name='mar_paj_no',
            field=models.CharField(blank=True, default='', help_text='PAJ number for Mar', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='pajln',
            name='may_paj_no',
            field=models.CharField(blank=True, default='', help_text='PAJ number for May', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='pajln',
            name='nov_paj_no',
            field=models.CharField(blank=True, default='', help_text='PAJ number for Nov', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='pajln',
            name='oct_paj_no',
            field=models.CharField(blank=True, default='', help_text='PAJ number for Oct', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='pajln',
            name='sep_paj_no',
            field=models.CharField(blank=True, default='', help_text='PAJ number for Sep', max_length=20, null=True),
        ),
    ]
