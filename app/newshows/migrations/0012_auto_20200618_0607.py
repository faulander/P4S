# Generated by Django 3.0.7 on 2020-06-18 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newshows', '0011_auto_20200617_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='show',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Show'),
        ),
        migrations.AlterField(
            model_name='show',
            name='url',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
    ]
