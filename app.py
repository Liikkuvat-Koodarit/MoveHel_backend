from dburi import db_uri
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
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
    review_list = []
    for r in reviews:
        review_list.append(format_review(r))
    return {"reviews": review_list}

# Yksittäisen arvostelun haku
@app.route("/review/<int:id>", methods=["GET"])
def get_review(id):
    review = Review.query.filter_by(id_review = id).one()
    formatted_review = format_review(review)
    return {"review": formatted_review}

# Yksittäisen arvostelun poisto
@app.route("/review/<int:id>", methods=["DELETE"])
def delete_review(id):
    try:
        review = Review.query.get(id)
        if review:
            db.session.delete(review)
            db.session.commit()
            return f"Review (id: {id}) deleted!"
        else:
            return f"Review with id {id} not found", 404
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        return f"Error deleting review: {str(e)}", 500
    finally:
        db.session.close()

# Yksittäisen arvostelun muokkaus
@app.route("/review/<int:id>", methods=["PUT"])
def update_review(id):
    try:
        review = Review.query.filter_by(id_review=id).first()
        if review:
            reviewText = request.json.get("reviewText")  # Use .get() to avoid KeyError if 'reviewText' is missing
            if reviewText is not None:
                review.reviewText = reviewText
                review.created_at = datetime.utcnow()  # Update the created_at timestamp
                db.session.commit()
                return {"review": format_review(review)}
            else:
                return {"error": "Missing 'reviewText' in request body"}, 400
        else:
            return {"error": "Review not found"}, 404
    except exc.SQLAlchemyError as e:
        return f"Error updating review with id {id}: {str(e)}", 500
    finally:
        db.session.close()

if __name__ == '__main__':
    app.run()
