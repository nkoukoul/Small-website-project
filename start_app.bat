cd %~dp0
CALL venv\Scripts\activate
SET FLASK_APP=movie_rama.py
flask run -h localhost -p 5000
