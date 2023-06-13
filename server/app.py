#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# 1. import flask_restful and Api, Resource
# 2. create POST, PATCH, DELETE for Reviews and OneReview

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
