#!/bin/bash

python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt

chown -R ec2-user:nginx /var/www

# Note: assuming port 8080 is open, you can test that the app will 
# run under uwsgi manually using the following
# uwsgi --socket 0.0.0.0:8080 --protocol=http -w wsgi:app

mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf-orig
cp config/nginx.conf /etc/nginx/nginx.conf

cp config/flaskapp.conf /etc/nginx/conf.d/flaskapp.conf

cp config/flaskapp.service /etc/systemd/system/flaskapp.service

mkdir /var/log/uwsgi
chown -R ec2-user:nginx /var/log/uwsgi

systemctl start flaskapp.service
systemctl enable flaskapp.service

systemctl restart nginx
systemctl enable nginx

export FLASK_APP=wsgi
flask db upgrade

echo 'Install complete'