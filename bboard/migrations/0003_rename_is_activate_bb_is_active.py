# Generated by Django 4.2.7 on 2024-04-04 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0002_rename_is_active_bb_is_activate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bb',
            old_name='is_activate',
            new_name='is_active',
        ),
    ]
