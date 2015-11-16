# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bet', '0010_auto_20150823_1035'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bet',
            options={'ordering': ('-date_time',)},
        ),
    ]
