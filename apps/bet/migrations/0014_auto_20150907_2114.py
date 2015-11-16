# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('bet', '0013_auto_20150907_2102'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='song',
            new_name='position',
        ),
        migrations.AlterField(
            model_name='comment',
            name='votes',
            field=models.ManyToManyField(related_name='votes', null=True, through='bet.Vote', to=settings.AUTH_USER_MODEL),
        ),
    ]
