# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('title', models.TextField()),
                ('ahjo_id', models.BigIntegerField(unique=True)),
                ('modified_time', models.DateTimeField(null=True)),
                ('last_decision_time', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='IssueSubscription',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('issue', models.ForeignKey(to='app.Issue')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('text', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now=True)),
                ('issue', models.ForeignKey(to='app.Issue')),
            ],
        ),
        migrations.CreateModel(
            name='MessageVote',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('vote_value', models.IntegerField()),
                ('message', models.ForeignKey(to='app.Message')),
            ],
        ),
        migrations.CreateModel(
            name='UserWithProfile',
            fields=[
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, primary_key=True, serialize=False)),
                ('description', models.TextField()),
                ('picture', models.ImageField(upload_to='image_uploads', blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='messagevote',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='poster',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='reply_to',
            field=models.ForeignKey(to='app.Message', related_name='replies', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='issuesubscription',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='subscriptions'),
        ),
        migrations.AlterUniqueTogether(
            name='messagevote',
            unique_together=set([('message', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='issuesubscription',
            unique_together=set([('issue', 'user')]),
        ),
    ]
