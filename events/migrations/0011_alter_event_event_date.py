# Generated by Django 4.2.1 on 2023-05-05 11:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_alter_event_event_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 5, 11, 2, 38, 357140)),
        ),
    ]
