# Generated by Django 3.1.5 on 2021-02-05 23:00

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_auto_20210205_0429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='date_bid',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 5, 23, 0, 56, 969169, tzinfo=utc), verbose_name='Date Bid'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='date_posted',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 5, 23, 0, 56, 968558, tzinfo=utc), verbose_name='Date Posted'),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 5, 23, 0, 56, 966415, tzinfo=utc), verbose_name='date joined'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(default='', verbose_name='Listing Description')),
                ('date_posted', models.DateTimeField(default=datetime.datetime(2021, 2, 5, 23, 0, 56, 970189, tzinfo=utc), verbose_name='Date Posted')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='auctions.listing')),
            ],
        ),
    ]
