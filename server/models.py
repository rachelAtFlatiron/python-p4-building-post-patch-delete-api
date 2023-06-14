from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()

'''
1. create columns for each table
2. create relationships between tables starting with Review
3. write serializer rules
'''

class Game(db.Model, SerializerMixin):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    #columns
    title = db.Column(db.String, unique=True)
    genre = db.Column(db.String)
    platform = db.Column(db.String)
    price = db.Column(db.Integer)
    
    #relationships
    game_reviews = db.relationship('Review', back_populates='game')
    #'user' is coming from Review.user
    '''
    First argument is the name of the relationship, second argument is the attribute in the other table that you want to associate
    '''
    users = association_proxy('game_reviews', 'user')

    #serializers
    serialize_rules = ('-game_reviews.game', '-created_at', '-updated_at')

    #repr
    def __repr__(self):
        return f'<Game {self.title} for {self.platform}>'
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''
game: 
    game_reviews:
        <----SERIALIZER RULE SAYS STOP---->
        review where review.game:
            game_reviews:
                review where review.game:
                    game_reviews
'''


class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # columns
    score = db.Column(db.Integer)
    comment = db.Column(db.String)

    #use table name for ForeignKey
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # relationships
    game = db.relationship('Game', back_populates='game_reviews')
    user = db.relationship('User', back_populates='user_reviews')
    # serializers: avoid max recursion
    serialize_rules = ('-user.user_reviews', '-game.game_reviews', '-updated_at', '-created_at')

    # repr
    def __repr__(self):
        return f'<Review ({self.id}) of {self.game}: {self.score}/10>'

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # columns
    name = db.Column(db.String)

    # relationships
    user_reviews  = db.relationship('Review', back_populates='user')
    #'game' refers to Review.game
    games = association_proxy('user_reviews', 'game')

    # serializers
    serialize_rules = ('-updated_at', '-created_at', '-user_reviews.user')

    # repr
    def __repr__(self):
        return f'<User name={self.name} />'