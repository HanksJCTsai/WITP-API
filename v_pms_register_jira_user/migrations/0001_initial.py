# Generated by Django 3.2.6 on 2022-03-21 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VPmsRegisterJiraUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(help_text='User Name', max_length=50)),
                ('employee_id', models.CharField(help_text='Employee ID', max_length=20, null=True)),
                ('email', models.TextField(help_text='E-Mail', unique=True)),
                ('status', models.IntegerField(default=1, help_text='Status')),
                ('create_date', models.DateTimeField(auto_now_add=True, help_text='Create Date')),
                ('deleted_date', models.DateTimeField(help_text='Deleted Date', null=True)),
                ('org_role', models.CharField(help_text='Organization Role', max_length=10, null=True)),
                ('jira_user_id', models.CharField(help_text='Jira User ID', max_length=100, null=True)),
                ('add_to_org_date', models.DateTimeField(auto_now_add=True, help_text='Add into Org Date', null=True)),
                ('last_seen_in_jira', models.DateTimeField(help_text='Last Seen In Jira Date', null=True)),
            ],
            options={
                'db_table': 'v_pms_register_jira_user',
                'ordering': ['id'],
            },
        ),
        # migrations.CreateModel(
        #     name='VPmsRegisterJiraUser',
        #     fields=[
        #         ('id', models.AutoField(primary_key=True, serialize=False)),
        #         ('user_name', models.CharField(help_text='User Name', max_length=50)),
        #         ('employee_id', models.CharField(help_text='Employee ID', max_length=20, null=True)),
        #         ('email', models.TextField(help_text='E-Mail', unique=True)),
        #         ('status', models.IntegerField(default=1, help_text='Status')),
        #         ('create_date', models.DateTimeField(auto_now_add=True, help_text='Create Date')),
        #         ('deleted_date', models.DateTimeField(help_text='Deleted Date', null=True)),
        #         ('org_role', models.CharField(help_text='Organization Role', max_length=10, null=True)),
        #         ('jira_user_id', models.CharField(help_text='Jira User ID', max_length=100, null=True)),
        #         ('add_to_org_date', models.DateTimeField(auto_now_add=True, help_text='Add into Org Date', null=True)),
        #         ('last_seen_in_jira', models.DateTimeField(help_text='Last Seen In Jira Date', null=True)),
        #     ],
        #     options={
        #         'db_table': 'v_pms_register_jira_user',
        #         'ordering': ['id'],
        #     },
        # ),
    ]
