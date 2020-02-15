
import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from config import database_setup, SQLALCHEMY_TRACK_MODIFICATIONS

#----------------------------------------------------------------------------#
# Database Setup 
#----------------------------------------------------------------------------#

database_path = "postgres://{}:{}@{}/{}".format(database_setup["user_name"], database_setup["password"], database_setup["port"], database_setup["database_name_production"])

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
  '''binds a flask application and a SQLAlchemy service'''
  app.config["SQLALCHEMY_DATABASE_URI"] = database_path
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS
  db.app = app
  db.init_app(app)
  db.create_all()

def db_drop_and_create_all():
    '''drops the database tables and starts fresh

    can be used to initialize a clean database
    '''
    db.drop_all()
    db.create_all()
    db_init_records()

def db_init_records():
    '''this will initialize the database with some test examples.'''
    new_actor = (Actor(
        name = 'Matthew',
        gender = 'Male',
        age = 25
        ))
    new_actor.insert()

#----------------------------------------------------------------------------#
# Example Model 
#----------------------------------------------------------------------------#

#TODO: Create Model Schema for App

class Actor(db.Model):  
  __tablename__ = 'actors'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  gender = Column(String)
  age = Column(Integer)

  def __init__(self, name, gender, age):
    self.name = name
    self.gender = gender
    self.age = age

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name' : self.name,
      'gender': self.gender,
      'age': self.age
    }