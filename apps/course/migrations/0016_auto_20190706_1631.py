# Generated by Django 2.2.2 on 2019-07-06 16:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0015_auto_20190706_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name=''),
        ),
    ]
