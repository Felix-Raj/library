# Generated by Django 2.0.5 on 2018-07-28 14:29

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lib_users', '0004_remove_libusers_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='libusers',
            name='avatar',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
        ),
    ]