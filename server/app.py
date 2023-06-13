#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, User, Review, Game

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

api = Api(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# 1. import flask_restful and Api, Resource
# 2. create POST, PATCH, DELETE for Reviews and OneReview

class Reviews(Resource):
    def get(self):
        q = Review.query.all()
        return make_response([r.to_dict(rules=('-user_id', '-game_id')) for r in q], 200)
    
    def post(self):
        data = request.get_json()
        review = Review(score=data.get('score'), comment=data.get('comment'), game_id=data.get('game_id'), user_id=data.get('user_id'))
        db.session.add(review)
        db.session.commit()

        return make_response(review.to_dict(), 201)

api.add_resource(Reviews, '/reviews')

class OneReview(Resource):
    def get(self, id):
        q = Review.query.filter_by(id=id).first()
        return make_response(q.to_dict(rules=('-user_id', '-game_id')), 200)
    
    def delete(self, id):
        q = Review.query.filter_by(id=id).first()
        db.session.delete(q)
        db.session.commit()
        return make_response({}, 204)
    
    def patch(self, id):
        q = Review.query.filter_by(id=id).first()
        data = request.get_json()
        for attr in data:
            setattr(q, attr, data.get(attr))
        db.session.add(q)
        db.session.commit()
        return make_response(q.to_dict(), 200)

api.add_resource(OneReview, '/reviews/<int:id>')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`

class Games(Resource):
    def get(self):
        q = Game.query.all()
        return make_response([g.to_dict(rules=('-reviews.user_id', '-reviews.game_id')) for g in q], 200)
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
