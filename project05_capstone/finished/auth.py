import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from config import auth0_config

#----------------------------------------------------------------------------#
# Auth0 Config
#----------------------------------------------------------------------------#

AUTH0_DOMAIN = auth0_config['AUTH0_DOMAIN']
ALGORITHMS = auth0_config['ALGORITHMS']
API_AUDIENCE = auth0_config['API_AUDIENCE']

#----------------------------------------------------------------------------#
# AuthError Exception
#----------------------------------------------------------------------------#
class AuthError(Exception):
    '''A standardized way to communicate auth failure modes'''
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code
    
#----------------------------------------------------------------------------#
# Auth Wrapper Methods
#----------------------------------------------------------------------------#

def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header

    *Input: None
    *Output:
       <string> token (part of the header)
    
    Conditions for Output:
       - Authorization header is available
       - header must not be malformed (i.e. Bearer XXXXX)

    """
    auth = request.headers.get('Authorization', None)
    # Raise error if no "Authorization" is part of header
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()
    # Raise error if no "Bearer" is part "Authorization"
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    # Raise error if "Authorization" only contains 1 part (it should have 2)
    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    # Raise error if "Authorization" contains more than 2 parts (it should only have 2)
    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    # When everyhting is fine, get the token which is the second part of the Authorization Header & return it
    return parts[1]

def check_permissions(permission, payload):
    ''' Check if permission is part of payload
    *Input
        <string> permission (i.e. 'post:example')
        <string> payload (decoded jwt payload)
    *Output:
         <bool> True if all conditions have been met
    
    Conditions for Output:
      - permissions are included in the payload
      - requested permission string is in the payload permissions array

    '''
    if 'permissions' not in payload:
                        raise AuthError({
                            'code': 'invalid_claims',
                            'description': 'Permissions not included in JWT.'
                        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)
    return True

def verify_decode_jwt(token):
    ''' Decodes JWT Token or raises appropiate Error Messages

    *Input
        <string> token (a json web token)
    
    *Output 
        <string> decoded payload

    Conditions for output to be returned:
        - Auth0 token with key id (key id = kid)
        - verify the token using Auth0 /.well-known/jwks.json
        - decode the payload from the token with Auth Config on top of auth.py
        - claims need to fit

    '''
    # Verify token
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    
    # Check if Key id is in unverified header
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    rsa_key = {} # initialize empty private rsa key as dict
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            # Use Auth Config (top of file) to decode JWT and return payload if succesful
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload

        # Raise Error if token is not valide anymore.
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        # Raise Error if token is claiming wrong audience.
        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)

        # In all other Error cases, give generic error message
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)

    # If no payload has been returned yet, raise error.
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)


# TODO DONE implement @requires_auth(permission) decorator method

def requires_auth(permission=''):
    ''' Authentification Wrapper to decorate Endpoints with
    
    *Input:
        <string> permission (i.e. 'post:drink')

    uses the get_token_auth_header method to get the token
    uses the verify_decode_jwt method to decode the jwt
    uses the check_permissions method validate claims and check the requested permission

    return the decorator which passes the decoded payload to the decorated method
    '''
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(token)
            except:
                raise AuthError({
                    'code': 'unauthorized',
                    'description': 'Permissions not found'
                }, 401)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator