# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bet', '0006_betitem_odd'),
    ]

    operations = [
        migrations.AddField(
            model_name='bet',
            name='stake',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
