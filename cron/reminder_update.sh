#!/bin/bash

echo "[START CRONTAB]"
cd /home/watervibe
python manage.py add_reminders
echo "[END CRONTAB]"
