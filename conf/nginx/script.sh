sudo apt-get install nginx -y
sudo cp tms.nepse.bot.conf /etc/nginx/sites-available/tms.nepse.bot
sudo ln -s  /etc/nginx/sites-available/data.nepse.bot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx