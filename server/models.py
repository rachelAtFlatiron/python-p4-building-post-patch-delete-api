from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()

'''
1. create columns for each table
2. create relationships between tables starting with Review
    - examine creator argument
3. write serializer rules (START IN REVIEW TO AVOID MAX RECURSION)
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
    reviews = db.relationship('Review', back_populates='game')
        # creator is used to create new instances of the associated class when adding elements to the proxy attribute
        # users is a proxy attribute
        # allows us to access and manipulate user attribute associated with Review objects
        # lambda creates new Review object with the given user
    #users = association_proxy('reviews', 'user', creator = lambda usr: Review(user=usr))
    users = association_proxy('reviews', 'user')

    #serializers
        # -reviews.game to avoid repeating information
    serialize_rules = ('-updated_at', '-created_at', '-reviews.game')

    #repr
    def __repr__(self):
        return f'<Game {self.title} for {self.platform}>'
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # columns
    score = db.Column(db.Integer)
    comment = db.Column(db.String)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # relationships
    game = db.relationship('Game', back_populates='reviews')
    user = db.relationship('User', back_populates='reviews')

    # serializers: avoid max recursion
    serialize_rules = ('-game.reviews', '-user.reviews', '-updated_at', '-created_at')
    

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
    reviews = db.relationship('Review', back_populates='user')
        # creator is used to create new instances of the associated class when adding elements to the proxy attribute
        # users is a proxy attribute
        # allows us to access and manipulate user attribute associated with Review objects
        # lambda creates new Review object with the given user
    #games = association_proxy('reviews', 'game', creator = lambda gm: Review(game = gm))
    games = association_proxy('reviews', 'game')
    
    # serializers
        # -reviews.user to avoid repeating information
    serialize_rules = ('-updated_at', '-created_at', '-reviews.user')


    def __repr__(self):
        return f'<User name={self.name} />'