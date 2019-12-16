import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

#----------------------------------------------------------------------------#
# App Setup
#----------------------------------------------------------------------------#

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
TODO DONE uncomment the following line to initialize the database
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

#----------------------------------------------------------------------------#
# Custom Functions
#----------------------------------------------------------------------------#

def get_error_message(error, default_text):
    '''Returns default error text or custom error message (if not applicable)
    Parameters:
        * <error> system generated error message which contains a description message
        * <string> default text to be used as error message if Error has no specific message

    Returns:
        * <string> specific error message or default text(if no specific message is given)

    '''
    try:
        # Return message contained in error, if possible
        return error.description["message"]
    except TypeError:
        # otherwise, return given default text
        return default_text

def get_all_drinks(recipe_format):
    '''Queries a formatted list of drinks with long or short recipt description

    *Input:
        <string> recipe_format "long" or "short", depending on how detailled the informations are needed
    
    *Output:
        <list> Formatted instances of Drinks

    If no drinks could be found, abort with 404 error.

    '''
    
    # Get all drinks in database
    all_drinks = Drink.query.order_by(Drink.id).all()

    # Format with different recipe detail level
    if recipe_format.lower() == 'short':
        all_drinks_formatted = [Drink.short(drink) for drink in all_drinks]
    elif recipe_format.lower() == 'long':
        all_drinks_formatted = [Drink.long(drink) for drink in all_drinks]
    else:
        return abort(500, {'message': 'bad formatted function call. recipe_format needs to be "short" or "long".'})

    if len(all_drinks_formatted) == 0:
        abort(404, {'message': 'no drinks found in database.'})
    
    # Return formatted list of drinks
    return all_drinks_formatted

#----------------------------------------------------------------------------#
# Endpoints
#----------------------------------------------------------------------------#

'''
TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks' methods=['GET'])
def drinks():
    """Returns all drinks
    """
    return jsonify({
    'success': True,
    'drinks': get_all_drinks('short')
    })


'''
TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks-detail' methods=['GET'])
def drinks_detail():
    """Returns all drinks with detailled recipe information
    """
    
    return jsonify({
    'success': True,
    'drinks': get_all_drinks('long')
    })

'''
TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


'''
TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


'''
TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


#----------------------------------------------------------------------------#
# Error Handlers
#----------------------------------------------------------------------------#

'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": get_error_message(error,"unprocessable")
                    }), 422

'''
TODO DONE implement error handlers using the @app.errorhandler(error) decorator
each error handler should return (with approprate messages):
    jsonify({
        "success": False, 
        "error": 404,
        "message": "resource not found"
        }), 404

'''

'''
TODO DONE implement error handler for 404
    error handler should conform to general task above 
'''
@app.errorhandler(404)
def ressource_not_found(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": get_error_message(error, "resource not found")
                    }), 404

'''
TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
