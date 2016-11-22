#!/bin/bash

echo "Running sync..."
cd /home/watervibe
python manage.py sync
python manage.py sync_new_user
