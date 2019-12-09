"""
Contains all Database configuration, models and relationships.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from config import SQLALCHEMY_DATABASE_URI # Import local database URI from Config File

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

# TODO DONE: Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
# Instead of creating a new Table, the documentation recommends to create a association table
Show = db.Table('Show', db.Model.metadata,
    db.Column('Venue_id', db.Integer, db.ForeignKey('Venue.id')),
    db.Column('Artist_id', db.Integer, db.ForeignKey('Artist.id')),
    db.Column('start_time', db.DateTime)
)

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    # TODO DONE: implement any missing fields, as a database migration using Flask-Migrate
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    genres = db.Column(db.ARRAY(db.String())) # To store multiple Genres, I decided to create an Array Column with String as Datatype
    seeking_description = db.Column(db.String(500)) # Because descriptions can be a little bit longer, I decided to accept input up to 500 characters
    venues = db.relationship('Artist', secondary=Show, backref=db.backref('shows', lazy='joined'))
    def __repr__(self):
        return 'Venue Id:{} | Name: {}'.format(self.id, self.name)

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    # TODO DONE: implement any missing fields, as a database migration using Flask-Migrate
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    genres = db.Column(db.ARRAY(db.String())) # To store multiple Genres, I decided to create an Array Column with String as Datatype
    seeking_description = db.Column(db.String(500)) # Because descriptions can be a little bit longer, I decided to accept input up to 500 characters

    def __repr__(self):
        return 'Artist Id:{} | Name: {}'.format(self.id, self.name)