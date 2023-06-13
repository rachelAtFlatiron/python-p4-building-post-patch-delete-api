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
    
    #relationships

    #serializers

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

    # relationships

    # serializers: avoid max recursion

    # repr
    def __repr__(self):
        return f'<Review ({self.id}) of {self.game}: {self.score}/10>'

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # columns

    # relationships

    # serializers

    # repr
    def __repr__(self):
        return f'<User name={self.name} />'