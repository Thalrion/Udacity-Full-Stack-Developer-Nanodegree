import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import AuthError, requires_auth
from models import db_drop_and_create_all, setup_db, Actor, Movie, Performance
from config import pagination

ROWS_PER_PAGE = pagination['example']

def create_app(test_config=None):
  '''create and configure the app'''
  
  app = Flask(__name__)
  setup_db(app)
  # db_drop_and_create_all() # uncomment this if you want to start a new database on app refresh

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

  def get_error_message(error, default_text):
      '''Returns default error text or custom error message (if not applicable)

      *Input:
          * <error> system generated error message which contains a description message
          * <string> default text to be used as error message if Error has no specific message
      *Output:
          * <string> specific error message or default text(if no specific message is given)

      '''
      try:
          # Return message contained in error, if possible
          return error['description']
      except TypeError:
          # otherwise, return given default text
          return default_text

  def paginate_results(request, selection):
    '''Paginates and formats database queries

    Parameters:
      * <HTTP object> request, that may contain a "page" value
      * <database selection> selection of objects, queried from database
    
    Returns:
      * <list> list of dictionaries of objects, max. 10 objects

    '''
    # Get page from request. If not given, default to 1
    page = request.args.get('page', 1, type=int)
    
    # Calculate start and end slicing
    start =  (page - 1) * ROWS_PER_PAGE
    end = start + ROWS_PER_PAGE

    # Format selection into list of dicts and return sliced
    objects_formatted = [object_name.format() for object_name in selection]
    return objects_formatted[start:end]

  #----------------------------------------------------------------------------#
  #  API Endpoints
  #  ----------------------------------------------------------------
  #  NOTE:  For explanation of each endpoint, please have look at the README.md file. 
  #         DOC Strings only contain short description and list of test classes 
  #----------------------------------------------------------------------------#

  #----------------------------------------------------------------------------#
  # Endpoint /actors GET/POST/DELETE/PATCH
  #----------------------------------------------------------------------------#
  @app.route('/actors', methods=['GET'])
  @requires_auth('read:actors')
  def get_actors(payload):
    """Returns paginated actors object

    Tested by:
      Success:
        - test_get_all_actors
      Error:
        - test_error_405_get_actors

    """
    selection = Actor.query.all()
    actors_paginated = paginate_results(request, selection)

    if len(actors_paginated) == 0:
      abort(404, {'message': 'no examples found in database.'})

    return jsonify({
      'success': True,
      'actors': actors_paginated
    })

  @app.route('/actors', methods=['POST'])
  @requires_auth('create:actors')
  def insert_actors(payload):
    """Inserts a new Actor

    Tested by:
      Success:
        - test_create_new_actor
      Error:
        - test_error_422_get_actors

    """
    # Get request json
    body = request.get_json()

    # Extract name and age value from request body
    name = body.get('name', None)
    age = body.get('age', None)

    # Set gender to value or to 'Other' if not given
    gender = body.get('gender', 'Other')

    # abort if one of these are missing with appropiate error message
    if not name:
      abort(422, {'message': 'no name provided.'})

    if not age:
      abort(422, {'message': 'no age provided.'})

    # Create new instance of Actor & insert it.
    new_actor = (Actor(
          name = name, 
          age = age,
          gender = gender
          ))
    new_actor.insert()

    return jsonify({
      'success': True,
      'created': new_actor.id
    })

  #----------------------------------------------------------------------------#
  # Error Handlers
  #----------------------------------------------------------------------------#

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
                        "success": False, 
                        "error": 422,
                        "message": get_error_message(error,"unprocessable")
                        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
                        "success": False, 
                        "error": 400,
                        "message": get_error_message(error, "resource not found")
                        }), 400

    @app.errorhandler(404)
    def ressource_not_found(error):
        return jsonify({
                        "success": False, 
                        "error": 404,
                        "message": get_error_message(error, "resource not found")
                        }), 404


    @app.errorhandler(AuthError)
    def authentification_failed(AuthError): 
        return jsonify({
                        "success": False, 
                        "error": AuthError.status_code,
                        "message": get_error_message(AuthError.error, "authentification fails")
                        }), 401


  # After every endpoint has been created, return app
  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)