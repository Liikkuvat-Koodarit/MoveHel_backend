from dburi import db_uri
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

class Review(db.Model):
    id_review = db.Column(db.Integer, primary_key=True)
    id_sportsPlace = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    reviewText = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Review: {self.reviewText}"
    
    def __init__(self, id_sportsPlace, rating, reviewText):
        self.id_sportsPlace = id_sportsPlace
        self.rating = rating
        self.reviewText = reviewText

def format_review(review):
    return {
        "id_review": review.id_review,
        "id_sportsPlace": review.id_sportsPlace,
        "rating": review.rating,
        "reviewText": review.reviewText,
        "created_at": review.created_at
    }


# Testifunktio GET-pyyntöjä varten
@app.route('/')
def hello():
    return 'Hey!'

# Arvostelun luonti
@app.route('/review', methods = ['POST'])
def create_review():
    id_sportsPlace = request.json['id_sportsPlace']
    rating = request.json['rating']
    reviewText = request.json['reviewText']

    review = Review(id_sportsPlace, rating, reviewText)
    
    db.session.add(review)
    db.session.commit()
    
    return format_review(review)

# Kaikkien arvostelujen haku
@app.route("/review", methods = ["GET"])
def get_reviews():
    reviews = Review.query.order_by(Review.created_at.asc()).all()

if __name__ == '__main__':
    app.run()
