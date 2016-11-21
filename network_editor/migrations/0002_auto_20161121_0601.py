# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network_editor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='edge',
            name='end_node',
            field=models.ForeignKey(related_name='end_node', default=None, to='network_editor.Node'),
        ),
        migrations.AlterField(
            model_name='edge',
            name='start_node',
            field=models.ForeignKey(related_name='start_node', default=None, to='network_editor.Node'),
        ),
    ]
