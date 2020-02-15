import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, db_drop_and_create_all, Actor, Movie, Performance
from config import database_setup
from sqlalchemy import desc

#----------------------------------------------------------------------------#
# Setup of Unittest
#----------------------------------------------------------------------------#

class AgencyTestCase(unittest.TestCase):
    """This class represents the agency test case"""

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

# Test driven development (TDD): Create testcases first, then add endpoints to pass tests

#----------------------------------------------------------------------------#
# Tests for /actors GET/POST/DELETE/PATCH
#----------------------------------------------------------------------------#
    def test_get_all_actors(self):
        """Test GET all actors."""
        res = self.client().get('/actors?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)

# Make the tests conveniently executable.
# From app directory, run 'python test_app.py' to start tests
if __name__ == "__main__":
    unittest.main()