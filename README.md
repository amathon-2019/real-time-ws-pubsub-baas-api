## Admin page server
real-time-ws-pubsub-bass-admin by team16

### Stack
Django, MySQL

### modify Settings.py
Connect your DB
Add Host

### install
```
git clone -b develop --single-branch https://github.com/amathon-2019/real-time-ws-pubsub-baas-api.git
cd real-time-ws-pubsub-baas-api
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### Watching Admin
```
localhost:8000/channel/
```

### update url
```
state 변경 url: http://localhost/channel/update_ServerState/<state>/
server수 변경 url: http://localhost/channel/update_ServerCount/<count>/
channel 갱신 url: http://localhost/channel/update_Channel/<name>/<client>/<rpm>/
```
### page view
<img width="641" alt="admin_page" src="https://user-images.githubusercontent.com/40608930/64088096-d2ed9300-cd7a-11e9-9331-a8b189bafead.PNG">

