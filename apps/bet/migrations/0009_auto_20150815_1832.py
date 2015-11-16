# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bet', '0008_auto_20150814_2127'),
    ]

    operations = [
        migrations.RenameField(
            model_name='song',
            old_name='youTube_link',
            new_name='youtube_link',
        ),
    ]
