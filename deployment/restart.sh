#!/bin/bash

source ~/waffle-rookies-19.5-backend-2/venv0/bin/activate
sudo fuser -k 8000/tcp
gunicorn --bind 0.0.0.0:8000 waffle_backend.wsgi:application -D
sudo nginx -t
sudo systemctl daemon-reload 
sudo service nginx restart
