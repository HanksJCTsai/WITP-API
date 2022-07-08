# Generated by Django 3.2.12 on 2022-03-22 03:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('imp_prf', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImpPrfln',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('project_year', models.CharField(default='', help_text='Project Year', max_length=4)),
                ('project_name', models.CharField(default='', help_text='Project Name', max_length=100)),
                ('div_group', models.CharField(default='', help_text='Division Group', max_length=30)),
                ('jan_plan', models.FloatField(help_text='Plan HC on Jan')),
                ('feb_plan', models.FloatField(help_text='Plan HC on feb')),
                ('mar_plan', models.FloatField(help_text='Plan HC on mar')),
                ('apr_plan', models.FloatField(help_text='Plan HC on apr')),
                ('may_plan', models.FloatField(help_text='Plan HC on may')),
                ('jun_plan', models.FloatField(help_text='Plan HC on June')),
                ('jul_plan', models.FloatField(help_text='Plan HC on July')),
                ('aug_plan', models.FloatField(help_text='Plan HC on aug')),
                ('sep_plan', models.FloatField(help_text='Plan HC on sep')),
                ('oct_plan', models.FloatField(help_text='Plan HC on oct')),
                ('nov_plan', models.FloatField(help_text='Plan HC on nov')),
                ('dec_plan', models.FloatField(help_text='Plan HC on dec')),
                ('creater', models.CharField(blank=True, default='', help_text='PRFLN Creater', max_length=50, null=True)),
                ('creatdate', models.DateTimeField(blank=True, null=True)),
                ('updater', models.CharField(blank=True, default='', help_text='PRFLN Updater', max_length=50, null=True)),
                ('updatedate', models.DateTimeField(blank=True, null=True)),
                ('prf', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imp_prf.impprf')),
            ],
            options={
                'db_table': 'imp_prfln',
                'unique_together': {('id', 'project_year', 'project_name', 'div_group')},
            },
        ),
    ]
