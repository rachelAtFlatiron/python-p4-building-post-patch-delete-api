#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#flask_restful
from flask_restful import Api, Resource 

from models import db, User, Review, Game

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app) #enable flask_restful

@app.route('/')
def index():
    return "Index for Game/Review/User API"

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# 1. import flask_restful and Api, Resource
# 2. create POST, PATCH, DELETE for Reviews and OneReview

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`

# name Reviews so as not to get confused with model Review 
# otherwise you will see this error:
# AttributeError: type object Review has no attribute query
class Reviews(Resource):
    def get(self):
        q = Review.query.all()
        rev_list = []
        for r in q:
            rev_list.append(r.to_dict())
        res = make_response(rev_list, 200)
        return res
    def post(self):
        #1. get data
        data = request.get_json()
        #2. create instance
        review = Review(score=data.get('score'), comment=data.get('comment'), game_id=data.get('game_id'), user_id=data.get('user_id'))
        #3. add review to db
        db.session.add(review)
        db.session.commit()
        #4. return response
        return make_response(review.to_dict(), 201)

# don't forget to add_resource
# or you will see a 404
api.add_resource(Reviews, '/reviews')

class OneReview(Resource):
    def get(self, review_id):
        q = Review.query.filter_by(id=review_id).first()
        return make_response(q.to_dict(), 200)
    
    def delete(self, review_id):
        # 1. get the query/instance
        q = Review.query.filter_by(id=review_id).first()
        # 2. delete from database
        db.session.delete(q)
        db.session.commit()
        # 3. send response
        return make_response({}, 204)
    
    def patch(self, review_id):
        # 1. get the query/instance
        review = Review.query.filter_by(id=review_id).first()
        # 2. get data
        data = request.get_json()
        # 3. update query
        for attr in data:
            setattr(review, attr, data.get(attr))
        # 4. save to db
        db.session.add(review)
        db.session.commit()
        # 5. return response
        return make_response(review.to_dict(), 200)
        
api.add_resource(OneReview, '/reviews/<int:review_id>')

class Games(Resource):
    def get(self):
        q = Game.query.all()
        # may see this error if missing comma at end of rules tuple
        # Game object has no attribute r
        return make_response([g.to_dict(rules=('-game_reviews', )) for g in q], 200)
api.add_resource(Games, '/games')

class OneGame(Resource):
    def get(self, id):
        q = Game.query.filter_by(id=id).first()
        return make_response(q.to_dict(rules=('-reviews.user_id', '-reviews.game_id')), 200)
api.add_resource(OneGame, '/games/<int:id>')

class Users(Resource):
    def get(self):
        q = User.query.all()
        return make_response([u.to_dict(rules=('-reviews.user_id', '-reviews.game_id')) for u in q], 200)
api.add_resource(Users, '/users')

class OneUser(Resource):
    def get(self, id):
        q = User.query.filter_by(id=id).first()
        return make_response(q.to_dict(rules=('-reviews.user_id', '-reviews.game_id')), 200)
api.add_resource(OneUser, '/users/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
