# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bet', '0007_bet_stake'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bet',
            old_name='user',
            new_name='better',
        ),
    ]
