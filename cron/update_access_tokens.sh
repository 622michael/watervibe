#!/bin/bash

echo '[START CRONTAB]'
cd /home/watervibe
python manage.py update_access_tokens
echo '[END CRONTAB]'