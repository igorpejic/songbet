# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bet', '0018_auto_20160112_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='youtube_link',
            field=models.CharField(max_length=300, null=True, blank=True),
        ),
    ]
