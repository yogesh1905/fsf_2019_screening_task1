# Generated by Django 2.1.7 on 2019-03-15 18:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0008_assigntask_group_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assigntask',
            name='group_id',
        ),
    ]
