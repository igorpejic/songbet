# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bet', '0015_auto_20151004_1931'),
    ]

    operations = [
        migrations.AddField(
            model_name='betitem',
            name='correct_choice',
            field=models.CharField(blank=True, max_length=5, null=True, choices=[(b'1', b'Will rise'), (b'X', b'Will stay'), (b'2', b'Will fall')]),
        ),
        migrations.AlterField(
            model_name='position',
            name='change',
            field=models.CharField(blank=True, max_length=4, null=True, choices=[(b'1', b'Has risen'), (b'X', b'Has stayed'), (b'2', b'Has fallen'), (b'N', b'New entry')]),
        ),
    ]
