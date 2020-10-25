git pull
cd /home/www/code/iman-game-bot
/home/www/code/iman-game-bot/venv/bin/python /home/www/code/iman-game-bot/manage.py migrate
sudo supervisorctl restart iman iman_worker
