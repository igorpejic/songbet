# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bet', '0017_position_n_change'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='performance_gain',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='week',
            name='airplay_gain',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='week',
            name='digital_gain',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='week',
            name='highest_ranking_debut',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='week',
            name='stream_gain',
            field=models.IntegerField(default=-1),
        ),
    ]
