# Generated by Django 3.1.1 on 2020-09-02 10:02

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_auto_20200902_0936'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='executiontime',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 2, 10, 2, 20, 552350, tzinfo=utc)),
        ),
    ]