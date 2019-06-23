# Meet&Eat #

App to find people with common interests to eat together. 
Сhoose place, time and topic and enjoy your meal with perfect companion!


### How to set up PostgreSQL (quick guide) ###

Until we set up a server for our DB we have to install everything locally. Therefore I also insert the password here visibly.
Use Version 10 or above. Make sure you also download the new settings.py.

##### Unix: #####

Download and install PostgreSQL and maybe pgAdmin for graphical interface.

Create DB via console:
```
$createdb -h localhost -p 5432 -U postgres meet_and_eat
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

1.Download PostgreSQL and open pgAdmin afterwards (comming with the installation)
2.Open pgAdmin
3.Create new DB/Server
4.Port:5432
5.Host: localhost
6.User: postgres
7.PAssword: postgres
8.Name: meet_and_eat

Afterwards you can access the DB via IntelliJ or DBeaver.
Make you you use 'python manage.py migrate' after adding a new model.

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

### Dependencies ###

##### Django-select2 #####

Library: Installing 'Tag-Filter': 
In python console:

pip install django2_select

##### Django-cleanup #####
pip install django-cleanup

##### python-decouple #####
pip install python-decouple

