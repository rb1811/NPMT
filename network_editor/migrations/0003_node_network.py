# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('network_editor', '0002_auto_20161121_0601'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='network',
            field=models.ForeignKey(default=80, to='network_editor.Network'),
            preserve_default=False,
        ),
    ]
