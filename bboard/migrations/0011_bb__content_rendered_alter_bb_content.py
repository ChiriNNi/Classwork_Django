# Generated by Django 4.2.7 on 2024-02-22 15:00

from django.db import migrations, models
import precise_bbcode.fields


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0010_revrubric'),
    ]

    operations = [
        migrations.AddField(
            model_name='bb',
            name='_content_rendered',
            field=models.TextField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='bb',
            name='content',
            field=precise_bbcode.fields.BBCodeTextField(blank=True, no_rendered_field=True, null=True, verbose_name='Описание'),
        ),
    ]