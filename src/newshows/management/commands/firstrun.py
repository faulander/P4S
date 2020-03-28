import os
import logging
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from newshows.models import Setting
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.core.management import call_command

logger = logging.getLogger("p4s")

class Command(BaseCommand):
    help = 'Setup of cronjobs for P4S'
    def handle(self, *args, **options):
        site_settings, created = Setting.objects.get_or_create(
            pk=1,
            defaults={
                "page": 0,
                "firstrun": True,
            }
        )
        if created:
            logger.info(f"Empty settings created.")
        schedule, created = IntervalSchedule.objects.get_or_create(every=1,period=IntervalSchedule.MINUTES)
        task, created = PeriodicTask.objects.get_or_create(
            name='Check for Active Sonarr',
            defaults={
                "interval":schedule,
                "task":"newshows.tasks.checkForActiveSonarr",
            }
       )
        task, created = PeriodicTask.objects.get_or_create(
            name='Get the list of TV Shows from TV Maze',
            defaults={
                "interval":schedule,
                "task":"newshows.tasks.HelperUpdateTVMaze",
            }
        )

        schedule, created = IntervalSchedule.objects.get_or_create(every=5,period=IntervalSchedule.MINUTES)
        task, created = PeriodicTask.objects.get_or_create(
            name='Get the latest Sonarr Downloads',
            defaults={
                "interval":schedule,
                "task":"newshows.tasks.getSonarrDownloads",
            }
        )
        task, created = PeriodicTask.objects.get_or_create(
            name='Get the latest Sonarr Profiles',
            defaults={
                "interval":schedule,
                "task":"newshows.tasks.helperGetSonarrProfiles",
            }
        )
        task, created = PeriodicTask.objects.get_or_create(
            name='Get the latest Sonarr Downloads',
            defaults={
                "interval":schedule,
                "task":"newshows.tasks.HelperUpdateSonarr",
            }
        )

        schedule, created = IntervalSchedule.objects.get_or_create(every=1,period=IntervalSchedule.DAYS)
        task, created = PeriodicTask.objects.get_or_create(
            name='Update local TV Maze Database',
            defaults={
                "interval":schedule,
                "task":"newshows.tasks.HelperUpdateShows",
            }
        )
        # Load show data into database if present
    site_settings = Setting.load()
    if site_settings.firstrun:
        call_command('loaddata', 'shows.json', app_label='newshows')
        site_settings.firstrun = False
        site_settings.save()