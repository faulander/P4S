#!/bin/sh

#First run
echo -e " \e[32m===============================================================================================\e[0m"
echo -e " \e[32mP4S - Migrate Database\e[0m"
python app/manage.py migrate --noinput
echo -e " \e[32m===============================================================================================\e[0m"
echo -e " \e[32mP4S - Create Superuser, Login: admin, Password: admin\e[0m"
python app/manage.py loaddata create_superuser
echo -e " \e[32m===============================================================================================\e[0m"
echo -e " \e[32mP4S - Importing Shows from June 2020\e[0m"
python app/manage.py loaddata showdata
echo -e " \e[32m===============================================================================================\e[0m"
echo -e " \e[32mP4S - Setup Webserver\e[0m"
python app/manage.py collectstatic --no-input --clear
echo -e " \e[32m===============================================================================================\e[0m"
echo -e " \e[32mP4S - Running locally\e[0m"
python app/manage.py runserver 7000 --noreload

