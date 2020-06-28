import os
import logging
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from newshows.models import Setting

logger = logging.getLogger(__name__)

class Command(BaseCommand):
  pass