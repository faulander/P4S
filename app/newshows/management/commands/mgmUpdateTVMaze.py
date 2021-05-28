from django.core.management.base import BaseCommand
from django.utils import timezone
from newshows.tasks import HelperUpdateTVMaze


class Command(BaseCommand):
    help = "manually updates TVMaze"

    def handle(self, *args, **kwargs):
        HelperUpdateTVMaze()
