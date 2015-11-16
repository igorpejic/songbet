# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bet', '0011_auto_20150823_1047'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=5000)),
                ('creator', models.ForeignKey(related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('song', models.ForeignKey(to='bet.Week')),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kind', models.CharField(default=b'null', max_length=8, choices=[(b'like', b'Like'), (b'dislike', b'Dislike'), (b'null', b'null')])),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('comment', models.ForeignKey(to='bet.Comment')),
                ('voter', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='votes',
            field=models.ManyToManyField(related_name='votes', through='bet.Vote', to=settings.AUTH_USER_MODEL),
        ),
    ]
