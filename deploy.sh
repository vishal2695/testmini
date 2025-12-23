#!/bin/bash
set -e

# 1️⃣ project folder me jao
cd /var/www/testmini

# 2️⃣ virtualenv activate karo
source /var/www/mini_venv/bin/activate

# 3️⃣ git se latest code pull karo
git pull origin master

# 4️⃣ dependencies install karo
pip install -r requirements.txt

# 5️⃣ django migrate aur collectstatic
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# 6️⃣ restart supervisor (Gunicorn)
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart mini
