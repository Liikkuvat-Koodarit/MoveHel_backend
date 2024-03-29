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

class appUser(db.Model):
    __tablename__ = 'appUser'
    id_user = db.Column(db.Integer, primary_key=True)
    usr_username = db.Column(db.String(100), nullable=False)
    usr_passwrd = db.Column(db.String(255), nullable=False)
    usr_email = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=0)

    def __repr__(self):
        return f"User: {self.usr_username}"
    
    def __init__(self, id_user, usr_username, usr_passwrd, usr_email, is_admin):
        self.id_user = id_user
        self.usr_username = usr_username
        self.usr_email = usr_email
        self.usr_passwrd = usr_passwrd
        self.is_admin = is_admin

def format_user(appUser):
    return {
        "userId": appUser.id_user,
        "userName": appUser.usr_username,
        "email": appUser.usr_email,
        "is_admin": appUser.is_admin
    }

class Review(db.Model):
    __tablename__ = 'review'
    id_review = db.Column(db.Integer, primary_key=True, autoincrement = True)
    id_sportsPlace = db.Column(db.Integer, nullable=False)
    name_sportsPlace = db.Column(db.String, nullable=True, default="noName")
    rating = db.Column(db.Integer, nullable=False)
    reviewText = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Review: {self.reviewText}"
    
    def __init__(self, id_sportsPlace, name_sportsPlace, rating, reviewText):
        self.id_sportsPlace = id_sportsPlace
        self.name_sportsPlace = name_sportsPlace
        self.rating = rating
        self.reviewText = reviewText     

def format_review(review):
    return {
        "reviewId": review.id_review,
        "sportsPlaceId": review.id_sportsPlace,
        "sportsPlaceName": review.name_sportsPlace,
        "rating": review.rating,
        "reviewText": review.reviewText,
        "createdAt": review.created_at
    }

# Arvostelun luonti
@app.route("/review", methods = ["POST"])
def add_review():
    data = request.get_json()

    sportsPlaceId = data.get('sportsPlaceId')
    sportsPlaceName = data.get('sportsPlaceName')
    rating = data.get('rating')
    reviewText = data.get('reviewText')

    if sportsPlaceId is None or rating is None or reviewText is None:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        review = Review(id_sportsPlace=sportsPlaceId, name_sportsPlace=sportsPlaceName, rating=rating, reviewText=reviewText)
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

#yhden liikuntapaikan kaikkien arvostelujen haku
# /location/review?sportsPlaceId=idNro
@app.route("/location/review", methods = ["GET"])
def get_reviews_location():
    try:
        sports_place_id = request.args.get('sportsPlaceId')

        # Check if sports place ID is provided
        if sports_place_id is None:
            return jsonify({"error": "Missing 'sportsPlaceId' parameter"}), 400
        
        reviews = Review.query.filter_by(id_sportsPlace=sports_place_id).order_by(Review.created_at.asc()).all()
        review_list = [format_review(r) for r in reviews]
        return {"reviews": review_list}
    except exc.SQLAlchemyError as e:
        return jsonify({"error": f"Error fetching reviews: {str(e)}"}), 500

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
            reviewText = request.json.get("reviewText")
            rating = request.json.get("rating")
            if reviewText is not None:
                review.reviewText = reviewText
                review.rating = rating
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

#käyttäjän luonti
@app.route("/user", methods = ["POST"])
def create_user():
    data = request.get_json()

    userId = data.get('userId')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    is_admin = data.get('is_admin')

    if username is None:
        return jsonify({"error": "Username is required."}), 400
    elif password is None:
         return jsonify({"error": "Password is required."}), 400
    elif email is None:
        return jsonify({"error": "Email is required."}), 400

    try:
        user = appUser(id_user=userId ,usr_username=username, usr_passwrd=password, usr_email=email, is_admin=is_admin)
        db.session.add(user)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"Error creating user: {str(e)}"}), 500        
    return format_user(user), 201

#yksittäisen käyttäjän haku
@app.route("/user/<int:id>", methods=["GET"])
def get_user(id):
    try:
        user = appUser.query.filter_by(id_user=id).one()
        formatted_user = format_user(user)
        return {"User": formatted_user}
    except exc.NoResultFound as e:
        return jsonify({"Error": f"User with id {id} not found: {str(e)}"}), 404

#yksittäisen käyttäjän muokkaus
@app.route("/user/<int:id>", methods=["PUT"])
def update_user(id):
    try:
        user = appUser.query.get(id)
        if user:
            username = request.json.get("username")
            password = request.json.get("password")
            email = request.json.get("email")
            if username is not None:
                user.usr_username = username
                user.usr_passwrd = password
                user.usr_email = email
                db.session.commit()
                return {"User": format_user(user)}
            else:
                return {"Error": "Missing 'username' in request body"}, 400
        else:
            return {"Error": "Review not found"}, 404
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        return f"Error updating review with id {id}: {str(e)}", 500
    finally:
        db.session.close()
            
#yksittäisen käyttäjän poisto
@app.route("/user/<int:id>", methods=["DELETE"])
def delete_user(id):
    try:
        user = appUser.query.get(id)
        if user:
            db.session.delete(user)
            db.session.commit() 
            return f"User (id_ {id}) deleted!"
        else:
            return f"User with id {id} not found", 404
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        return f"Error deleting user: {str(e)}", 500
    finally: db.session.close()

if __name__ == '__main__':
    app.run(port=5000, debug=True)
