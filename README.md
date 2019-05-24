Meet&Eat

App to find people with common interests to eat together. 
Сhoose place, time and topic and enjoy your meal with perfect companion!


How to set up PostgreSQL (quick guide):

Until we set up a server for our DB we have to install everything locally. Therefore I also insert the password here visibly.
Use Version 10 or above. Make sure you also download the new settings.py.

Unix:

1. Download and install PostgreSQL and maybe pgAdmin for graphical interface

--Create DB via console--

$createdb -h localhost -p 5432 -U postgres meet_and_eat

password should be set to 'postgres' by default

--pgAdmin--
1. Create new Server
2. Host: localhost
3. Port: 5432
4. User: postgres
5. Password: postgres
6.Name: meet_and_eat

Win:

1.Download PostgreSQL and open pgAdmin afterwards (comming with the installation)
2.Open pgAdmin
3.Create new DB/Server
4.Port:5432
5.Host: localhost
6.User: postgres
7.PAssword: postgres
8.Name: meet_and_eat