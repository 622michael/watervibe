#!/bin/bash
export DJANGO_SETTINGS_MODULE=watervibe.settings

echo '[START CRONTAB]'
cd /home/watervibe
python manage.py update_access_tokens
echo '[END CRONTAB]'
