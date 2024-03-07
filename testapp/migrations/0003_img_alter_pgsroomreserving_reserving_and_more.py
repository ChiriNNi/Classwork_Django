# Generated by Django 5.0.1 on 2024-02-29 14:02

import datetime
import django.contrib.postgres.fields.hstore
import django.contrib.postgres.fields.ranges
import django.contrib.postgres.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0002_pgsproject_pgsrubric_psgproject2_psgproject3_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Img',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='', verbose_name='Изображение')),
                ('desc', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Изображение',
                'verbose_name_plural': 'Изображения',
            },
        ),
        migrations.AlterField(
            model_name='pgsroomreserving',
            name='reserving',
            field=django.contrib.postgres.fields.ranges.DateTimeRangeField(validators=[django.contrib.postgres.validators.RangeMinValueValidator(limit_value=datetime.datetime(2000, 1, 1, 0, 0)), django.contrib.postgres.validators.RangeMaxValueValidator(limit_value=datetime.datetime(3000, 1, 1, 0, 0))], verbose_name='Время резервирования'),
        ),
        migrations.AlterField(
            model_name='psgproject2',
            name='platforms',
            field=django.contrib.postgres.fields.hstore.HStoreField(validators=[django.contrib.postgres.validators.KeysValidator(('client', 'server'), strict=True)], verbose_name='Использованные платформы'),
        ),
    ]