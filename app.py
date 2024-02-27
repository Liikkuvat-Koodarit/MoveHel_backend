from dburi import db_uri
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS # Cross-Origin Resource Sharing
from sqlalchemy import exc
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)
# CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:5173", "http://localhost:5000", "http://localhost:3000"]}})
CORS(app)

class Review(db.Model):
    __tablename__ = 'review'
    id_review = db.Column(db.Integer, primary_key=True, autoincrement = True)
    id_sportsPlace = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    reviewText = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Review: {self.reviewText}"
    
    def __init__(self, id_sportsPlace, rating, reviewText):
        self.id_sportsPlace = id_sportsPlace
        self.rating = rating
        self.reviewText = reviewText
        
    
def format_review(review):
    return {
        "reviewId": review.id_review,
        "sportsPlaceId": review.id_sportsPlace,
        "rating": review.rating,
        "reviewText": review.reviewText,
        "createdAt": review.created_at
    }

# Arvostelun luonti
@app.route("/review", methods = ["POST"])
def add_review():
    data = request.get_json()

    sportsPlaceId = data.get('sportsPlaceId')
    rating = data.get('rating')
    reviewText = data.get('reviewText')

    if sportsPlaceId is None or rating is None or reviewText is None:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        review = Review(id_sportsPlace=sportsPlaceId, rating=rating, reviewText=reviewText)
        db.session.add(review)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"Error adding review: {str(e)}"}), 500

    return format_review(review), 201

# Kaikkien arvostelujen haku
@app.route("/review", methods = ["GET"])
def get_reviews():
    try:
        reviews = Review.query.order_by(Review.created_at.asc()).all()
        review_list = [format_review(r) for r in reviews]
        return {"reviews": review_list}
    except exc.SQLAlchemyError as e:
        return jsonify({"error": f"Error fetching reviews: {str(e)}"}), 500

# Yksittäisen arvostelun haku
@app.route("/review/<int:id>", methods=["GET"])
def get_review(id):
    try:
        review = Review.query.filter_by(id_review=id).one()
        formatted_review = format_review(review)
        return {"review": formatted_review}
    except exc.NoResultFound as e:
        return jsonify({"error": f"Review with id {id} not found: {str(e)}"}), 404

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
        review = Review.query.filter_by(reviewId=id).first()
        if review:
            reviewText = request.json.get("reviewText")  # Use .get() to avoid KeyError if 'reviewText' is missing
            if reviewText is not None:
                review.reviewText = reviewText
                review.createdAt = datetime.utcnow()  # Update the createdat timestamp
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
    app.run(port=5000, debug=True)
