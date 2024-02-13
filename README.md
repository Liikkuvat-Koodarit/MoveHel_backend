# MoveHel Back-end

# Prerequisites
- Install Python 3.12.1 and PIP 23.2.1
- Install PostgreSQL 16
- Install pipenv: **pip install pipenv**
- Activate pipenv: **pipenv shell**
- Run your virtualenv path through Python interpreter
- Install pipenv dependencies: **pipenv install flask flask-sqlalchemy psycopg2 python-dotenv flask-cors**

# Running the app
- Move to the backend folder with **cd MoveHel_backend**
- In terminal: start the app with **flask run** 

# VSCode terminalissa komennot
>>> python
>>> from app import app, db
>>> app.app_context().push()
>>> db.create_all()

# pgAdmin
- Klikkaa oikealla **Databases -> Create -> Database**
- Nimeä **movehel -> Save** (HUOM! tietokannan nimi pitää olla sama kun dburi tiedostossa oleva.
db_uri = 'postgresql://postgres:OMA-SALASANA@localhost/**movehel**' eli toi viimeinen osa localhostin jälkeen pitää olla sama kun tietokannan nimi)
- Tietokannan taulut löytyy puuvalikosta: **Databases -> movehel -> Schemas -> Tables**
- Tietojen päivitys tapahtuu right-klikkaamalla ja painamalla Refresh