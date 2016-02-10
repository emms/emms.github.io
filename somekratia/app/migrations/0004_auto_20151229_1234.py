# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_issue_ahjo_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='category_name',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='issue',
            name='summary',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='message',
            name='issue',
            field=models.ForeignKey(to='app.Issue', related_name='messages'),
        ),
        migrations.AlterField(
            model_name='userwithprofile',
            name='picture',
            field=models.ImageField(default='app/static/default_avatar.png', upload_to='image_uploads'),
        ),
    ]
