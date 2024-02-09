from dburi import db_uri
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

class Review(db.Model):
    id_review = db.Column(db.Integer, primary_key=True)
    id_place = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'))  # Define foreign key
    user = db.relationship('User', backref='reviews')  # Define relationship
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Review: {self.description}"

class User(db.Model):
    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), nullable=False)

@app.route('/')
def hello():
    return 'Hey!'

if __name__ == '__main__':
    app.run()
