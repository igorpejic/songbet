# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bet', '0003_auto_20150802_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bet',
            name='has_won',
            field=models.CharField(default=b'Pending', max_length=20, choices=[(b'True', b'True'), (b'False', b'False'), (b'Pending', b'Pending')]),
        ),
        migrations.AlterField(
            model_name='betitem',
            name='choice',
            field=models.CharField(max_length=20, choices=[(b'1', b'Will rise'), (b'X', b'Will stay'), (b'2', b'Will fall')]),
        ),
    ]
