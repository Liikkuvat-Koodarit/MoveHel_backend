# MoveHel Back-end

## Prerequisites
1. Install Python 3.12.1 and PIP 23.2.1
2. Install PostgreSQL 16
3. Install pipenv: **pip install pipenv**
4. Activate pipenv: **pipenv shell**
5. Run your virtualenv path through Python interpreter
6. Install pipenv dependencies: **pipenv install flask flask-sqlalchemy psycopg2 python-dotenv flask-cors**

## Database creation
1. Right click: **Databases -> Create -> Database**
2. Name the database: **movehel -> Save** (NOTE! name of the database should be the same as the one in "dburi.py".
3. To create database tables, input the following commands in powershell **one by one**:
> python
> from app import app, db
> app.app_context().push()
> db.create_all()
> exit()

Local database URI for development:
- db_uri = "postgresql://postgres:YOUR_PASSWORD@localhost/**movehel**")

Database tables can be found like so: **Databases -> movehel -> Schemas -> Tables**
- Information can be refreshed by right clicking on a field and clicking **Refresh**

## Running the app
1. Move to the backend folder with **cd MoveHel_backend**
2. In terminal: start the app with **flask run**