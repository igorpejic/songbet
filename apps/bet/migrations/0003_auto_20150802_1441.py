# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bet', '0002_auto_20150721_2018'),
    ]

    operations = [
        migrations.CreateModel(
            name='BetItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('choice', models.CharField(max_length=20, choices=[(b'1', b'Will rise'), (b'x', b'Will stay'), (b'2', b'Will fall')])),
                ('bet', models.ForeignKey(to='bet.Bet')),
                ('song', models.ForeignKey(to='bet.Song')),
            ],
        ),
        migrations.RemoveField(
            model_name='listofbet',
            name='bet',
        ),
        migrations.RemoveField(
            model_name='listofbet',
            name='song',
        ),
        migrations.DeleteModel(
            name='ListOfBet',
        ),
    ]
