# AirportDatabase
A project for my Database Organization class.

The project was made using Pycharm.

AirlineDB.py is the main file of the project. 
-We used psycopg2 to connect it to our database. We linked it to a local postgres Database, so if you intend to test the code, you will need to change every psycopg2.connect() to your database.
-We used flask to connect to html templates in order to make the web application.

make_tables.py is a python file that creates all the tables. (It also contains a methond to delete all of them)

CS425Part2.sql contains all of our CREATE TABLE queries. (You can use this or make_tables.py to create the tables)

ERModel2.jpg is our ER design.

fauxdata.txt is the database test data. It is writen as SQL insertion operations. 

requirements.txt includes the installation of psycopg2.

Folder: "Templates" contains all of our Html templates.

Folder: "static" contains the CSS and javascript used to compliment our templates.
