# Generated by Django 3.2 on 2021-07-14 07:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('imp_div', '0001_initial'),
        ('imp_ib', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImpIbln',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('projectyear', models.CharField(default='', help_text='Project Year', max_length=4)),
                ('projectname', models.CharField(default='', help_text='Project Name', max_length=100)),
                ('janplan', models.FloatField(help_text='Plan HC on Jan')),
                ('febplan', models.FloatField(help_text='Plan HC on feb')),
                ('marplan', models.FloatField(help_text='Plan HC on mar')),
                ('aprplan', models.FloatField(help_text='Plan HC on apr')),
                ('mayplan', models.FloatField(help_text='Plan HC on may')),
                ('junplan', models.FloatField(help_text='Plan HC on June')),
                ('julplan', models.FloatField(help_text='Plan HC on July')),
                ('augplan', models.FloatField(help_text='Plan HC on aug')),
                ('sepplan', models.FloatField(help_text='Plan HC on sep')),
                ('octplan', models.FloatField(help_text='Plan HC on oct')),
                ('novplan', models.FloatField(help_text='Plan HC on nov')),
                ('decplan', models.FloatField(help_text='Plan HC on dec')),
                ('ibid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imp_ib.impib')),
                ('divid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imp_div.impdiv')),
            ],
            options={
                'db_table': 'imp_ibln',
                'unique_together': {('id', 'ibid', 'divid')},
            },
        ),
    ]
