# Generated by Django 2.1.7 on 2019-03-15 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_assigntask'),
    ]

    operations = [
        migrations.AddField(
            model_name='assigntask',
            name='group_id',
            field=models.IntegerField(default=-1),
        ),
    ]