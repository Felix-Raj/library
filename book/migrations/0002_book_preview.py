# Generated by Django 2.0.5 on 2018-07-28 15:29

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='preview',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
        ),
    ]
