import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import AuthError, requires_auth
from models import db_drop_and_create_all, setup_db, Example
from config import pagination

EXAMPLES_PER_PAGE = pagination['example']

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

  def paginate_questions(request, selection):
    '''Paginates and formats example 

    Parameters:
      * <HTTP object> request, that may contain a "page" value
      * <database selection> selection of examples, queried from database
    
    Returns:
      * <list> list of dictionaries of examples, max. 10 questions

    '''
    # Get page from request. If not given, default to 1
    page = request.args.get('page', 1, type=int)
    
    # Calculate start and end slicing
    start =  (page - 1) * EXAMPLES_PER_PAGE
    end = start + EXAMPLES_PER_PAGE

    # Format selection into list of dicts and return sliced
    examples = [example.format() for example in selection]
    return questions[start:end]

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
  @requires_auth('get:examples') # decorate this endpoint to require a 'get:examples' permission from Auth. Result is accessible via payload argument. Pass no argument if authentification is requiered, but no permission
  def example_get_endPoint(payload):
    """Returns 1 example object

    Tested by:
      Success:
        - test_get_all_examples
      Error:
        - test_error_405_get_all_examples

    """
    this_example = Example.query.all()

    if len(this_example) == 0:
      abort(404, {'message': 'no examples found in database.'})

    return jsonify({
      'success': True,
      'drinks': this_example
    })

  #----------------------------------------------------------------------------#
  # Error Handlers
  #----------------------------------------------------------------------------#

  @app.errorhandler(404)
  def ressource_not_found(error):
      return jsonify({
                      "success": False, 
                      "error": 404,
                      "message": get_error_message(error, "resource not found")
                      }), 404

  # After every endpoint has been created, return app
  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)