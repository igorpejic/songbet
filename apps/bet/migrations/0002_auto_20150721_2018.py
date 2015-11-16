# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bet', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Bet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('has_won', models.BooleanField(default=False)),
                ('bet_type', models.CharField(default=b'3', max_length=20, choices=[(b'1', b'Top 10'), (b'2', b'Top 20'), (b'3', b'1x2')])),
            ],
        ),
        migrations.CreateModel(
            name='Better',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('points', models.IntegerField(default=100)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Collaboration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('artist', models.ForeignKey(to='bet.Artist')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='ListOfBet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('choice', models.CharField(max_length=20, choices=[(b'1', b'Will rise'), (b'x', b'Will stay'), (b'2', b'Will fall')])),
                ('bet', models.ForeignKey(to='bet.Bet')),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.SmallIntegerField()),
            ],
            options={
                'ordering': ['week'],
            },
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('youTube_link', models.URLField(null=True, blank=True)),
                ('artist_name', models.CharField(max_length=250)),
                ('artist', models.ForeignKey(to='bet.Artist')),
            ],
        ),
        migrations.CreateModel(
            name='Week',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('songs', models.ManyToManyField(to='bet.Song', through='bet.Position')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.AddField(
            model_name='position',
            name='song',
            field=models.ForeignKey(to='bet.Song'),
        ),
        migrations.AddField(
            model_name='position',
            name='week',
            field=models.ForeignKey(to='bet.Week'),
        ),
        migrations.AddField(
            model_name='listofbet',
            name='song',
            field=models.ForeignKey(to='bet.Song'),
        ),
        migrations.AddField(
            model_name='genre',
            name='genre',
            field=models.ForeignKey(to='bet.Song'),
        ),
        migrations.AddField(
            model_name='collaboration',
            name='song',
            field=models.ForeignKey(to='bet.Song'),
        ),
        migrations.AddField(
            model_name='bet',
            name='user',
            field=models.ForeignKey(to='bet.Better'),
        ),
    ]
