# Generated by Django 4.2.7 on 2024-04-09 16:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0002_alter_bb_rubric'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bb',
            name='rubric',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='bboard.rubric', verbose_name='Рубрика'),
        ),
    ]
