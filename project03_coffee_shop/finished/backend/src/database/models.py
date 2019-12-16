import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple versions of a database
'''
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    db_init_records()

def db_init_records():
    '''This will initialize the database with some test drinks
    
    Called on every restart, after database has been reseted by db_drop_and_create_all()
    
    '''
    new_drink1 = (Drink(
                        id = 1,
                        title = 'matcha shake', 
                        recipe = """[
                                {
                                    "name" : "milk",
                                    "color": "grey",
                                    "parts": 1
                                },
                                {
                                    "name" : "matcha",
                                    "color": "green",
                                    "parts": 3
                                }
                        ]"""
                        ))

    new_drink2 = (Drink(
                        id = 2,
                        title = 'Purple Pain', 
                        recipe = """[
                                {   
                                    "name" : "guave",
                                    "color": "purple",
                                    "parts": 3
                                },
                                {
                                    "name": "milk",
                                    "color": "white",
                                    "parts": 2
                                }
                        ]"""
                        ))
    new_drink1.insert()               
    new_drink2.insert()

'''
Drink
a persistent drink entity, extends the base SQLAlchemy Model
'''
class Drink(db.Model):
    # Autoincrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    title = Column(String(80), unique=True)
    # the ingredients blob - this stores a lazy json blob
    # the required datatype is [{'color': string, 'name':string, 'parts':number}]
    recipe = Column(String(180), nullable=False)

    '''
    short()
        short form representation of the Drink model
    '''
    def short(self):
        short_recipe = [{'color': r['color'], 'parts': r['parts']} for r in json.loads(self.recipe)]
        return {
            'id': self.id,
            'title': self.title,
            'recipe': short_recipe
        }

    '''
    long()
        long form representation of the Drink model
    '''
    def long(self):
        try:
            return {
                'id': self.id,
                'title': self.title,
                'recipe': json.loads(self.recipe)
            }
        except:
            return {
                'id': self.id,
                'title': self.title,
                'recipe': self.recipe
            }

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            drink = Drink.query.filter(Drink.id == id).one_or_none()
            drink.title = 'Black Coffee'
            drink.update()
    '''
    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())