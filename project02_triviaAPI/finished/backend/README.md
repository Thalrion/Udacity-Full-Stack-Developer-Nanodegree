# Full Stack Trivia API Backend

1.  Start Project locally.
2.  API Documentation

## Start Project locally

Make sure that you `cd` into the backend folder before following the setup steps.
Also, you need the latest version of 

To start and run the local development server,

1. Initialize and activate a virtualenv:
  ```bash
  $ cd YOUR_PROJECT_DIRECTORY_PATH/
  $ virtualenv --no-site-packages env
  $ source env/bin/activate
  ```

2. Install the dependencies:
  ```bash
  $ pip install -r requirements.txt
  ```

3. With Postgres running, restore a database using the trivia.psql file provided.
    ```bash
    $ psql trivia < trivia.psql
    ```

4. Run the development server:
  ```bash 
  $ export FLASK_APP=flaskr
  $ export FLASK_ENV=development # enables debug mode
  $ flask run
  ```

>_tip_: Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

5. Testing
To run the tests, run
```bash 
$ dropdb trivia_test
$ createdb trivia_test
$ psql trivia_test < trivia.psql
$ python test_flaskr.py
```

## API Documentation

Here you can find all existing endpoints, which methods can be used, how to work with them & example responses you´ll get.

Additionally, common pitfalls & error messages are explained, if applicable.

### Base URL

Since this API is not hosted on a specific domain, it can only be accessed when
`flask` is run locally. To make requests to the API via `curl` or `postman`,
you need to use the default domain, on which the flask server is running

`

### Available Endpoints

Here is a short table about which ressources exist and which method you can use on them.

                          Allowed Methods
       Endpoints    |  GET |  POST |  DELETE | 
                    |------|------ |---------|
      /questions    |  [x] |  [x]  |   [x]   |         
      /categories   |  [x] |  [x]  |   [x]   |           
      /quizzes      |      |  [x]  |         | 


### How to work with each endpoint

Endpoints
1. GET      '/questions'
2. POST     '/questions'
3. DELETE   '/questions/<question_id>'
4. POST     '/quizzes'
5. GET      '/categories'
6. GET      '/categories/<category_id>/questions'
7. POST     '/categories'
8. DELETE   '/categories'


`GET '/questions'`

`GET '/categories'`
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 

Example Response:
```js
{
'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"
}
```

