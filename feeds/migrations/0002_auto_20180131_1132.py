# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import feeds.models


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feeds',
            name='publish',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='feeds',
            name='slug',
            field=models.SlugField(max_length=250, default='Feeds Title', unique_for_date='publish'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=feeds.models.UploadToPathAndRename('E:\\pro\\media/upload\\here')),
        ),
    ]
