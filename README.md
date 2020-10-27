Requirements:

Python 3 (has been tested with Python 3.6)


Sqlite was chosen as the database for reasons of simplicity
No deployement on application or web server included.
Application uses flask development server not suited for production
Deployment option includes gunicorn with gevent workers as application server
and nginx as web server

On windows 10

initial setup:
	initial_setup.bat
run application:
	start_app.bat

Details:
(python executable on cmd is py)

From file explorer go the project directory
Start command prompt there
Initialize virtual environment:
	py -m venv venv
activate virtual environment:
	venv\Scripts\activate
Install packages:
	pip install -r requirements.txt
Export application file
	SET FLASK_APP=movie_rama.py	
Start applications
	flask run -h localhost -p 5000
local host and port can be adjusted according to needs
 

On Linux

initial setup:
        initial_setup.sh
run application:
        start_app.sh

Details:
Initialize virtual environment:
        python3 -m venv venv
activate virtual environment:
        source venv/bin/activate
Install packages:
        pip install -r requirements.txt
Export application file
        export FLASK_APP=movie_rama.py
Start applications
        flask run -h localhost -p 5000
local host and port can be adjusted according to needs


In case you want to reset the database a migration framework is provided
The database is app.db
Remove the existing database
run:
flask db upgrade
