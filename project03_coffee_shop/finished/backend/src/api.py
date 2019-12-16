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
        return error['description']
    except TypeError:
        # otherwise, return given default text
        return default_text

def get_all_drinks(recipe_format):
    '''Queries a formatted list of drinks with long or short recipe description

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

def get_single_drink(drink_id):
    '''Queries a single drink with long recipe description and formats it

    *Input:
        <integer> id drink it to be queuried
    *Output:
        <list> Formatted instance of single Drink

    If drink with id could not be found, return 404.

    '''
    # Get drink with id
    single_drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    if not single_drink:
        abort(404, {'message': 'Drink with id {} not found in database.'.format(drink_id)})
    
    return Drink.long(single_drink)
#----------------------------------------------------------------------------#
# Endpoints
#----------------------------------------------------------------------------#

'''
TODO DONE implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks' , methods=['GET'])
def drinks():
    """Returns all drinks"""
    return jsonify({
    'success': True,
    'drinks': get_all_drinks('short')
    })


'''
TODO DONE implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks-detail',  methods=['GET'])
@requires_auth('get:drinks-detail')
def drinks_detail(payload):
    """Returns all drinks with detailed recipe information"""
    return jsonify({
    'success': True,
    'drinks': get_all_drinks('long')
    })

'''
TODO DONE implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks',  methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):
    """Creates new drink and returns it to client"""
    
    body = request.get_json()
    new_drink = Drink(title = body['title'], recipe = """{}""".format(body['recipe']))
    
    new_drink.insert()
    new_drink.recipe = body['recipe']
    return jsonify({
    'success': True,
    'drinks': Drink.long(new_drink)
    })

'''
TODO DONE implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>',  methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, drink_id):
    """Updates existing drink and returns it to client"""
    
    # Get body from request
    body = request.get_json()

    if not body:
      abort(400, {'message': 'request does not contain a valid JSON body.'})
    
    # Find drink which should be updated by id
    drink_to_update = Drink.query.filter(Drink.id == drink_id).one_or_none()

    # Check if and which fields should be updated
    updated_title = body.get('title', None)
    updated_recipe = body.get('recipe', None)
    
    # Depending on which fields are available, make apropiate updates
    if updated_title:
        drink_to_update.title = body['title']
    
    if updated_recipe:
        drink_to_update.recipe = """{}""".format(body['recipe'])
    
    drink_to_update.update()

    return jsonify({
    'success': True,
    'drinks': [Drink.long(drink_to_update)]
    })

'''
TODO DONE implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>',  methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(payload, drink_id):
    """Deletes 1 drink with given id"""
    if not drink_id:
        abort(422, {'message': 'Please provide valid drink id'})

    # Get drink with id
    drink_to_delete = Drink.query.filter(Drink.id == drink_id).one_or_none()

    if not drink_to_delete:
        abort(404, {'message': 'Drink with id {} not found in database.'.format(drink_id)})
     
    drink_to_delete.delete()
    
    return jsonify({
    'success': True,
    'delete': drink_id
    })

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
'''
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
                    "success": False, 
                    "error": 400,
                    "message": get_error_message(error, "resource not found")
                    }), 400
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
TODO DONE implement error handler for AuthError
    error handler should conform to general task above 
'''
@app.errorhandler(AuthError)
def authentification_failed(AuthError): 
    return jsonify({
                    "success": False, 
                    "error": AuthError.status_code,
                    "message": get_error_message(AuthError.error, "authentification fails")
                    }), 401