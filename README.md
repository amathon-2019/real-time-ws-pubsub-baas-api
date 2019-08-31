## Admin page server
real-time-ws-pubsub-bass-admin by team16

### Stack
Django, MySQL

### modify Settings.py
Connect your DB
Add Host

### install
```
git clone -b dev --single-branch https://github.com/amathon-2019/real-time-ws-pubsub-baas-api.git
cd real-time-ws-pubsub-baas-api
pip install requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### Watching Channel
```
localhost:8000/channel/
```


