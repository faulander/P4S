# Generated by Django 3.0.4 on 2020-03-20 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newshows', '0007_setting_last_tvmaze_full_update'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='SONARR_APIKEY',
            field=models.CharField(blank=True, default='Please enter your Sonarr API-Key', max_length=40, verbose_name='Sonarr API-Key'),
        ),
        migrations.AlterField(
            model_name='setting',
            name='SONARR_URL',
            field=models.CharField(blank=True, default='Please enter the full path to your SONARR API', max_length=1000, verbose_name='Sonarr URL'),
        ),
    ]
