# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, auto_now_add=True)),
                ('url', models.URLField(unique=True)),
                ('site_name', models.CharField(max_length=200, blank=True)),
                ('title', models.CharField(max_length=200, blank=True)),
                ('description', models.TextField(blank=True)),
                ('image', models.URLField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
