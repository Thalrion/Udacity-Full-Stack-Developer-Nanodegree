
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

#----------------------------------------------------------------------------#
# Example Model 
#----------------------------------------------------------------------------#

#TODO: Create Model Schema for App

class example(db.Model):  
  __tablename__ = 'examples'

  id = Column(Integer, primary_key=True)
  description = Column(String)

  def __init__(self, description):
    self.description = description

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
      'description': self.question
    }