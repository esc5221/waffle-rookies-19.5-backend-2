source ~/.bash_profile
cd ~/waffle-rookies-19.5-backend-2
git pull origin deploy
source venv0/bin/activate
cat requirements.txt | xargs -n 1 pip3 install
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py check --deploy
sudo fuser -k 8000/tcp
gunicorn --bind 0.0.0.0:8000 waffle_backend.wsgi:application -D
sudo nginx -t
sudo service nginx restart