# Generated by Django 3.1.1 on 2020-09-06 12:01

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0005_auto_20200903_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='executiontime',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 6, 12, 1, 39, 574937, tzinfo=utc)),
        ),
    ]
