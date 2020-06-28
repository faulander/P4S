#!/bin/sh

#Afterwards
docker-compose -f docker-compose.yml up -d
docker-compose -f docker-compose.yml exec -d web python manage.py qcluster
