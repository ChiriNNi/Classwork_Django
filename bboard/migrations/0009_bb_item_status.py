# Generated by Django 4.2.7 on 2023-12-19 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0008_alter_bb_options_alter_bb_order_with_respect_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='bb',
            name='item_status',
            field=models.CharField(choices=[('new', 'Новый'), ('used', 'Б/у'), ('refurbished', 'Восстановленный')], default='new', max_length=20, verbose_name='Состояние товара'),
        ),
    ]