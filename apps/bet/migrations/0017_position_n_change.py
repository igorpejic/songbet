# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bet', '0016_auto_20151004_2100'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='n_change',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
