# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('bet', '0014_auto_20150907_2114'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='change',
            field=models.CharField(default=1, max_length=4, choices=[(b'1', b'Has risen'), (b'X', b'Has stayed'), (b'2', b'Has fallen'), (b'N', b'New entry')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='votes',
            field=models.ManyToManyField(related_name='votes', through='bet.Vote', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='vote',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 4, 17, 31, 27, 962540, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
