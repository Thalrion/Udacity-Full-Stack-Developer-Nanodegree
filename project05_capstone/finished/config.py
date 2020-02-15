# This file should be included in .gitignore to not store sensitive data in version control
import os
SECRET_KEY = os.urandom(32)

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_TRACK_MODIFICATIONS = False

# TODO: Change values to your database setup information
database_setup = {
    "database_name_production" : "example",
    "database_name_test" : "example_test",
    "user_name" : "postgres", # default postgres user name
    "password" : "testpassword123", # if applicable. If no password, just type in None
    "port" : "localhost:5432" # default postgres port
}

# TODO: Change values with data from your Auth0 Dashboard
auth0_config = {
    "AUTH0_DOMAIN" : "example-matthew.eu.auth0.com",
    "ALGORITHMS" : ["RS256"],
    "API_AUDIENCE" : "Example"
}

pagination = {
    "example" : 10 # Limits returned rows of API
}
