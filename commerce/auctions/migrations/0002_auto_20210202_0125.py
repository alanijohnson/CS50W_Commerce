# Generated by Django 3.1.5 on 2021-02-02 01:25

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 2, 1, 25, 14, 371274, tzinfo=utc), verbose_name='date joined'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, null=True, unique=True, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=64, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=64, verbose_name='last name'),
        ),
    ]