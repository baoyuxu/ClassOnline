# Generated by Django 2.2.2 on 2019-07-06 07:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0013_auto_20190706_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 6, 15, 26, 50, 578209), verbose_name=''),
        ),
    ]
