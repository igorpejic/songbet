# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bet', '0004_auto_20150802_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='odd_1',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='position',
            name='odd_2',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='position',
            name='odd_x',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
