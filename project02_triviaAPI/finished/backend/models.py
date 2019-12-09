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
# Question Model 
#----------------------------------------------------------------------------#

class Question(db.Model):  
  __tablename__ = 'questions'

  id = Column(Integer, primary_key=True)
  question = Column(String)
  answer = Column(String)
  category = Column(String)
  difficulty = Column(Integer)

  def __init__(self, question, answer, category, difficulty):
    self.question = question
    self.answer = answer
    self.category = category
    self.difficulty = difficulty

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
      'question': self.question,
      'answer': self.answer,
      'category': self.category,
      'difficulty': self.difficulty
    }

#----------------------------------------------------------------------------#
# Category Model 
#----------------------------------------------------------------------------#

class Category(db.Model):  
  __tablename__ = 'categories'

  id = Column(Integer, primary_key=True)
  type = Column(String)

  def __init__(self, type):
    self.type = type

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'type': self.type
    }