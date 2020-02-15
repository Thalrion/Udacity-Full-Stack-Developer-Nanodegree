# TODO: Setup test suite and configuration with unittest
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Question, Category
from config import database_setup
from sqlalchemy import desc

#----------------------------------------------------------------------------#
# Setup of Unittest
#----------------------------------------------------------------------------#

class ExampleTestCase(unittest.TestCase):
    """This class represents the example test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        db_user = database_setup["user_name"]
        pwd = database_setup["password"]
        port = database_setup["port"]
        db_name = database_setup["database_name_test"]

        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = "postgres://{}:{}@{}/{}".format(db_user, pwd, port, db_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

#TODO: Create test cases