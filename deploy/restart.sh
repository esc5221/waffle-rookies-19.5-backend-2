cd ~/waffle-rookies-19.5-backend-2
source venv0/bin/activate
sudo fuser -k 8000/tcp
gunicorn --bind 0.0.0.0:8000 waffle_backend.wsgi:application -D
sudo nginx -t
sudo service nginx restart