from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dburi import db_uri

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key = true)
    description = db.Column(db.String(100), nullable = false)

@app.route('/')
def hello():
    return 'Hey!'

if __name__ == '__main__':
    app.run()