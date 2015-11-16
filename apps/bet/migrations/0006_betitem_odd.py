# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bet', '0005_auto_20150808_2234'),
    ]

    operations = [
        migrations.AddField(
            model_name='betitem',
            name='odd',
            field=models.FloatField(default=1.0),
            preserve_default=False,
        ),
    ]
