# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bet', '0009_auto_20150815_1832'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='position',
            options={'ordering': ['position']},
        ),
        migrations.AddField(
            model_name='bet',
            name='week',
            field=models.ForeignKey(default=1, to='bet.Week'),
            preserve_default=False,
        ),
    ]
