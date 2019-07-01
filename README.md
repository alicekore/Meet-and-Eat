# Meet&Eat #

App to find people with common interests to eat together.
Сhoose place, time and topic and enjoy your meal with perfect companion!
## Table of contents ##
1. [ DB. ](#db)
2. [ Roles. ](#roles)
3. [ Dependencies. ](#dependencies)
4. [ Mailing. ](#mailing)
5. [ Python-decouple and Environments. ](#python-decouple)
6. [ Dockerisation. ](#docker)
7. [ Backgroundtasks. ](#background-tasks)

<a name="db"></a>
### How to set up PostgreSQL (quick guide) ###

Until we set up a server for our DB we have to install everything locally. Therefore I also insert the password here visibly.
Use Version 10 or above. Make sure you also download the new settings.py.

##### Unix: #####

Download and install PostgreSQL and maybe pgAdmin for graphical interface.

Create DB via console:
```
createdb -h localhost -p 5432 -U postgres meet_and_eat
```
Password should be set to 'postgres' by default.


PgAdmin:

1. Create new Server
2. Host: localhost
3. Port: 5432
4. User: postgres
5. Password: postgres
6. Name: meet_and_eat

##### Win: #####

1. Download PostgreSQL and open pgAdmin afterwards (comming with the installation)
2. Open pgAdmin
3. Create new DB/Server
4. Port:5432
5. Host: localhost
6. User: postgres
7. PAssword: postgres
8. Name: meet_and_eat

Afterwards you can access the DB via IntelliJ or DBeaver.  
Make you you use `python manage.py migrate` after adding a new model.  
**Note:** If you experience some troubles with db, execute the following commands in the given order:  
```
python manage.py makemigrations  
python manage.py makemigrations meetandeat  
python manage.py migrate  
```
It helps sometimes

<a name="roles"></a>
### Roles ###

**Admin as superuser**

profile:
owner: can see all information and edit everything excempt from his username;
mod:-

dashboard:
user(owner): edit, see, join, leave events
user: see, leave,join,report events
mod: makes events in/-visible

Eventdetails:
user: access denied
user(joined): see, leave,join,report events
mod: -
user(owner): edit, see, join, leave events

<a name="dependencies"></a>
### Dependencies ###

##### Django-select2 #####

Library: Installing 'Tag-Filter':
In python console:
```
pip install django_select2
```
##### Django-cleanup #####
```
pip install django-cleanup
```
##### python-decouple #####
```
pip install python-decouple
```
<a name="mailing"></a>
### Mailing ###
By default, mailing is disabled. When you register, you won't get an email, but you will see an activation link in the server console.  
You can enable mailing in `meeteat/development-env/.env`

<a name="python-decouple"></a>
### Python Decouple and Environments ###
**Note:** you can still run the app with:  
`python manage.py runserver`  
python-decouple shouldn't affect the development process.  
python-decouple package provides an ability to set settings dynamic for different application environments. Some values in settings.py is set with python-decouple, the settings for different environments stored in /meeteat/meeteat/env

<a name="docker"></a>
### Dockerisation ###
**Note:** you can still run the app with:  
`python manage.py runserver`  
Docker shouldn't affect the development process.  
Dockerfile and docker-compose.yml let you run the app in the docker container. You need to have docker and docker-compose  
To build and run the containers run following commands in the folder with Dockerfile:  

`sudo docker-compose build`  
`sudo docker-compose up -d`  

You should be able to access application on 127.0.0.1:8000 after it.  
For debug purposes you can enter following commands:  
#Nginx  
`docker-compose logs nginx`  
#Web  
`docker-compose logs web`  
#DB  
`docker-compose logs db`  
You will see then logs of the corresponding containers  
**Note:** Email password is not in the docker config, because of security reasons. So if you want to test docker application set environment to development in the Dockerfile.    

<a name="background-tasks"></a>
### Background-tasks ###
for simple automation we can use a backgroundscheduler.
this will run tasks from 'tasks.py'.
tasks have to be added to 'updater.py'.
to run a task once app starts, run task in 'apps.py' ready() method.
**Note:** To make sure django only runs in one instance:  
`python manage.py runserver --noreload`  
