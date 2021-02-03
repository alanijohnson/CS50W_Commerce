# Generated by Django 3.1.5 on 2021-02-03 23:14

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20210203_0233'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auctions.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='listing',
            name='date_posted',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 3, 23, 14, 13, 22558, tzinfo=utc), verbose_name='Date Posted'),
        ),
        migrations.AddField(
            model_name='listing',
            name='description',
            field=models.TextField(default='', verbose_name='Listing Description'),
        ),
        migrations.AddField(
            model_name='listing',
            name='is_open',
            field=models.BooleanField(default=True, verbose_name='Open'),
        ),
        migrations.AddField(
            model_name='listing',
            name='title',
            field=models.CharField(default='', max_length=64, verbose_name='Listing Title'),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 3, 23, 14, 13, 20396, tzinfo=utc), verbose_name='date joined'),
        ),
    ]