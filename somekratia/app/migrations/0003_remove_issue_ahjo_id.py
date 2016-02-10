# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20151222_1433'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issue',
            name='ahjo_id',
        ),
    ]
