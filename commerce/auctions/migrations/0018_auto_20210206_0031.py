# Generated by Django 3.1.5 on 2021-02-06 00:31

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_auto_20210206_0023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='date_bid',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 6, 0, 31, 2, 24304, tzinfo=utc), verbose_name='Date Bid'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date_posted',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 6, 0, 31, 2, 25311, tzinfo=utc), verbose_name='Date Posted'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='auctions.category'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='date_posted',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 6, 0, 31, 2, 23694, tzinfo=utc), verbose_name='Date Posted'),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 6, 0, 31, 2, 21538, tzinfo=utc), verbose_name='date joined'),
        ),
    ]
