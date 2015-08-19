# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='tag',
            new_name='tags',
        ),
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.TextField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(),
            preserve_default=True,
        ),
    ]
