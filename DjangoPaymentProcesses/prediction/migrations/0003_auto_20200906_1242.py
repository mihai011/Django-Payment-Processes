# Generated by Django 3.1.1 on 2020-09-06 12:42

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('prediction', '0002_auto_20200906_1207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prediction',
            name='alias',
        ),
        migrations.RemoveField(
            model_name='prediction',
            name='name',
        ),
        migrations.AddField(
            model_name='prediction',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 9, 6, 12, 42, 48, 265668, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='prediction',
            name='value',
            field=models.FloatField(default=0.0),
        ),
    ]
