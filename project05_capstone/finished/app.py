import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

def create_app(test_config=None):
  '''create and configure the app'''
  
  app = Flask(__name__)

  #----------------------------------------------------------------------------#
  # CORS (API configuration)
  #----------------------------------------------------------------------------#

  CORS(app)
  # CORS Headers 
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response

  #----------------------------------------------------------------------------#
  # Custom Functions
  #----------------------------------------------------------------------------#

  def do_something():
    '''do something
    
    *Inputs:
        None
    *Outputs:
        None
    
    '''
    pass

  #----------------------------------------------------------------------------#
  #  API Endpoints
  #  ----------------------------------------------------------------
  #  NOTE:  For explanation of each endpoint, please have look at the README.md file. 
  #         DOC Strings only contain short description and list of test classes 
  #----------------------------------------------------------------------------#

  #----------------------------------------------------------------------------#
  # Endpoint /exampleGetEndPoint GET/POST/DELETE
  #----------------------------------------------------------------------------#

  @app.route('/exampleGetEndPoint', methods=['GET'])
  def get_questions():
    """Returns paginated questions

    Tested by:
      Success:
        - test_get_all_examples
      Error:
        - test_error_405_get_all_examples

    """

  # After every endpoint has been created, return app
  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)