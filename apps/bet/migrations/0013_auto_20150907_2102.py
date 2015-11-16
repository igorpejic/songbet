# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bet', '0012_auto_20150831_2054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='song',
            field=models.ForeignKey(to='bet.Position'),
        ),
    ]
