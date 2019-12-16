# Full Stack Trivia API Backend

1.  [Start Project locally](#start-project)
2.  [API Documentation](#api-documentation)

<a name="start-project"></a>
## Start Project locally

Make sure that you `cd` into the backend folder before following the setup steps.
Also, you need the latest version of [Python 3](https://www.python.org/downloads/)
and [postgres](https://www.postgresql.org/download/) installed on your machine.

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
$ createdb trivia
$ createdb trivia_test
$ psql trivia < trivia.psql
```

4. Change database config so it can connect to your local postgres database
- Open `config.py` with your editor of choice. 
- Here you can see this dict:
 ```python
 database_setup = {
    "database_name_production" : "trivia",
    "database_name_test" : "trivia_test",
    "user_name" : "postgres", # default postgres user name
    "password" : "mypassword123", # if applicable. If no password, just type in None
    "port" : "localhost:5432" # default postgres port
}
 ```
 - Just change `user_name`, `password` and `port` to whatever you choose while installing postgres.
>_tip_: `user_name` usually defaults to `postgres` and `port` always defaults to `localhost:5432` while installing postgres, most of the time you just need to change the `password`.

5. Run the development server:
  ```bash 
  $ export FLASK_APP=flaskr
  $ export FLASK_ENV=development # enables debug mode
  $ flask run
  ```

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

1. (optional) To execute tests, run
```bash 
$ dropdb trivia_test
$ createdb trivia_test
$ psql trivia_test < trivia.psql
$ python test_flaskr.py
```
If you choose to run all tests, it should give this response if everything went fine:
```bash
$ python test_flaskr.py
C:\Python36\lib\site-packages\sqlalchemy\util\langhelpers.py:217: 
  loader = self.auto_fn(name)
......................
----------------------------------------------------------------------
Ran 22 tests in 6.748s

OK

```

<a name="api-documentaton"></a>
## API Documentation

Here you can find all existing endpoints, which methods can be used, how to work with them & example responses you´ll get.

Additionally, common pitfalls & error messages are explained, if applicable.

### Base URL

Since this API is not hosted on a specific domain, it can only be accessed when
`flask` is run locally. To make requests to the API via `curl` or `postman`,
you need to use the default domain on which the flask server is running.

**_http://127.0.0.1:5000/_**

### Available Endpoints

Here is a short table about which ressources exist and which method you can use on them.

                          Allowed Methods
       Endpoints    |  GET |  POST |  DELETE | 
                    |------|-------|---------|
      /questions    |  [x] |  [x]  |   [x]   |         
      /categories   |  [x] |  [x]  |   [x]   |           
      /quizzes      |      |  [x]  |         | 


### How to work with each endpoint

Click on a link to directly get to the ressource.

1. Questions
   1. [GET /questions](#get-questions)
   2. [POST /questions](#post-questions)
   3. [DELETE /questions/<question_id>](#delete-questions)
2. Quizzes
   1. [POST /quizzes](#post-quizzes)
3. Categories
   1. [GET /categories](#get-categories)
   2. [GET /categories/<category_id>/questions](#get-categories-questions)
   3. [POST /categories](#post-categories)
   4. [DELETE /categories](#delete-categories)

Each ressource documentation is clearly structured:
1. Description in a few words
2. `curl` example that can directly be used in terminal
3. More descriptive explanation of input & outputs.
4. Example Response.
5. Error Handling (`curl` command to trigger error + error response)

# <a name="get-questions"></a>
### 1. GET /questions

Fetch paginated questions:
```bash
$ curl -X GET http://127.0.0.1:5000/questions?page=1
```
- Fetches a list of dictionaries of questions in which the keys are the ids with all available fields, a list of all categories and number of total questions.
- Request Arguments: 
    - **integer** `page` (optional, 10 questions per page, defaults to `1` if not given)
- Request Headers: **None**
- Returns: 
  1. List of dict of questions with following fields:
      - **integer** `id`
      - **string** `question`
      - **string** `answer`
      - **string** `category`
      - **integer** `difficulty`
  2. **list** `categories`
  3. **list** `current_category`
  4. **integer** `total_questions`
  5. **boolean** `success`

#### Example response
```js
{
"categories": [
    "Science",
    "Art",
    "Geography",
    "History",
    "Entertainment",
    "Sports"
  ],
"current_category": [
    "Science",
    "Art",
    "Geography",
    "History",
    "Entertainment",
    "Sports"
  ],
"questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },

 [...]

  ],
  "success": true,
  "total_questions": 19
}

```
#### Errors
If you try fetch a page which does not have any questions, you will encounter an error which looks like this:

```bash
curl -X GET http://127.0.0.1:5000/questions?page=12452512
```

will return

```js
{
  "error": 404,
  "message": "resource not found",
  "success": false
}

```

# <a name="post-questions"></a>
### 2. POST /questions

Search Questions
```bash
curl -X POST http://127.0.0.1:5000/questions -d '{"searchTerm" : "test"}' -H 'Content-Type: application/json'
```

Create new Question
```bash
curl -X POST http://127.0.0.1:5000/questions -d '{ "question" : "Is this a test question?", "category" : "1" , "answer" : "Yes it is!", "difficulty" : 1 }' -H 'Content-Type: application/json'
```

- Searches database for questions with a search term, if provided. Otherwise,
it will insert a new question into the database.
- Request Arguments: **None**
- Request Headers :
  - if you want to **search** (_application/json_)
       1. **string** `searchTerm` (<span style="color:red">*</span>required)
  - if you want to **insert** (_application/json_) 
       1. **string** `question` (<span style="color:red">*</span>required)
       2. **string** `answer` (<span style="color:red">*</span>required)
       3. **string** `category` (<span style="color:red">*</span>required)
       4. **integer** `difficulty` (<span style="color:red">*</span>required)
- Returns: 
  - if you searched:
    1. List of dict of `questions` which match the `searchTerm` with following fields:
        - **integer** `id`
        - **string** `question`
        - **string** `answer`
        - **string** `category`
        - **integer** `difficulty`
    2. List of dict of ``current_category`` with following fields:
        - **integer** `id`
        - **string** `type`
    3. **integer** `total_questions`
    4. **boolean** `success`
  - if you inserted:
    1. List of dict of all questions with following fields:
        - **integer** `id` 
        - **string** `question`
        - **string** `answer`
        - **string** `category`
        - **integer** `difficulty`
    2. **integer** `total_questions`
    3. **integer** `created`  id from inserted question
    4. **boolean** `success`

#### Example response
Search Questions
```js
{
  "current_category": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },

   [...] // all current categories

  ],
  "questions": [
    {
      "answer": "Jup",
      "category": 1,
      "difficulty": 1,
      "id": 24,
      "question": "Is this a test question?"
    }

    [...] // + all questions which contain the search term in its question
  
  ],
  "success": true,
  "total_questions": 20
}

```
Create Question
```js
{
  "created": 26, // id of question created
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
   
   [...] // + all questions in database

  ],
  "success": true,
  "total_questions": 21
}

```


#### Errors
**Search related**

If you try to search for a `question` which does not exist, it will response with an `404` error code:

```bash
curl -X POST http://127.0.0.1:5000/questions -d '{"searchTerm" : "this does not exist"}' -H'Content-Type: application/json' 
```

will return

```js
{
  "error": 404,
  "message": "No questions that contains \"this does not exist\" found.",
  "success": false
}
```
**Insert related**

If you try to insert a new `question`, but forget to provide a required field, it will throw an `400` error:
```bash
curl -X POST http://127.0.0.1:5000/questions -d '{ "question" : "Is this a question without an answer?", "category" : "1" , "difficulty" : 1 }' -H 'Content-Type: application/json'
```

will return

```js
{
  "error": 400,
  "message": "Answer can not be blank",
  "success": false
}
```
# <a name="delete-questions"></a>
### 3. DELETE /questions/<question_id>

Delete Questions
```bash
curl -X DELETE http://127.0.0.1:5000/questions/10
```
- Deletes specific question based on given id
- Request Arguments: 
  - **integer** `question_id`
- Request Headers : **None**
- Returns: 
    - **integer** `deleted` Id from deleted question.
    - **boolean** `success`


#### Example response
```js
{
  "deleted": 10,
  "success": true
}
```

### Errors

If you try to delete a `question` which does not exist, it will throw an `400` error:

```bash
curl -X DELETE http://127.0.0.1:5000/questions/7
```
will return
```js
{
  "error": 400,
  "message": "Question with id 7 does not exist.",
  "success": false
}
```

# <a name="post-quizzes"></a>
### 4. POST /quizzes

Play quiz game.
```bash
curl -X POST http://127.0.0.1:5000/quizzes -d '{"previous_questions" : [1, 2, 5], "quiz_category" : {"type" : "Science", "id" : "1"}} ' -H 'Content-Type: application/json'
```
- Plays quiz game by providing a list of already asked questions and a category to ask for a fitting, random question.
- Request Arguments: **None**
- Request Headers : 
     1. **list** `previous_questions` with **integer** ids from already asked questions
     1. **dict** `quiz_category` (optional) with keys:
        1.  **string** type
        2. **integer** id from category
- Returns: 
  1. Exactly one `question` as **dict** with following fields:
      - **integer** `id`
      - **string** `question`
      - **string** `answer`
      - **string** `category`
      - **integer** `difficulty`
  2. **boolean** `success`

#### Example response
```js
{
  "question": {
    "answer": "Jup",
    "category": 1,
    "difficulty": 1,
    "id": 24,
    "question": "Is this a test question?"
  },
  "success": true
}

```
### Errors

If you try to play the quiz game without a a valid JSON body, it will response with an  `400` error.

```bash
curl -X POST http://127.0.0.1:5000/quizzes
```
will return
```js
{
  "error": 400,
  "message": "Please provide a JSON body with previous question Ids and optional category.",
  "success": false
}

```
# <a name="get-categories"></a>
### 5. GET /categories

Fetch all available categories

```bash
curl -X GET http://127.0.0.1:5000/categories
```

- Fetches a list of all `categories` with its `type` as values.
- Request Arguments: **None**
- Request Headers : **None**
- Returns: A list of categories with its `type` as values
and a `success` value which indicates status of response. 

#### Example response
```js
{
  "categories": [
    "Science",
    "Art",
    "Geography",
    "History",
    "Entertainment",
    "Sports"
  ],
  "success": true
}
```
### Errors

Endpoint does not raise any specific errors.

# <a name="get-categories-questions"></a>
### 6. GET /categories/<category_id>/questions

Get all questions from a specific `category`.
```bash
curl -X GET http://127.0.0.1:5000/categories/2/questions?page=1
```
- Fetches all `questions` (paginated) from one specific category.
- Request Arguments:
  - **integer** `category_id` (<span style="color:red">*</span>required)
  - **integer** `page` (optinal, 10 questions per Page, defaults to `1` if not given)
- Request Headers: **None**
- Returns: 
  1. **integer** `current_category` id from inputted category
  2. List of dict of all questions with following fields:
     - **integer** `id` 
     - **string** `question`
     - **string** `answer`
     - **string** `category`
     - **integer** `difficulty`
  3. **integer** `total_questions`
  4. **boolean** `success`

#### Example response

```js
{
  "current_category": "2",
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ],
  "success": true,
  "total_questions": 4
}
```

### Errors
This endpoint can yield 2 common errors. For example, if you ask for questions of a category that does not exist it will throw an `400` error:
```bash
curl -X GET http://127.0.0.1:5000/categories/10/questions?page=1
```
will return
```bash
{
  "error": 400,
  "message": "No questions with category 10 found.",
  "success": false
}
```
Additionally, if you query for a category which has questions, but not on the selected `page`, it will raise an `404` error:
```bash
curl -X GET http://127.0.0.1:5000/categories/1/questions?page=5
```
will return
```bash
{
  "error": 404,
  "message": "No questions in selected page.",
  "success": false
}

```
# <a name="post-categories"></a>
### 7. POST /categories

Create new category.
```bash
curl -X POST http://127.0.0.1:5000/categories -d '{ "type" : "Nerd Stuff"}' -H 'Content-Type: application/json'
```

- Inserts a new `category` to extend gameplay with new kind of questions.
- Request Arguments: **None**
- Request Headers : (_application/json_) 
   1. **string** type (<span style="color:red">*</span>required)
- Returns: 
  1. List of dict of all existing `categories` with following fields:
      - **integer** `id` 
      - **string** `type`
  2. **integer** `total_categories` number of all `categories`
  3. **integer** `created`  id from inserted `category`
  4. **boolean** `success`

#### Example response
```js
{
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"
    },
    {
      "id": 4,
      "type": "History"
    },
    {
      "id": 5,
      "type": "Entertainment"
    },
    {
      "id": 6,
      "type": "Sports"
    },
    {
      "id": 7,
      "type": "Nerd Stuff"
    }
  ],
  "created": 7,
  "success": true,
  "total_categories": 7
}
```


#### Errors

If you try to insert a new category without `type` field, it will throw an `400` error:
```bash
curl -X POST http://127.0.0.1:5000/categories -d '{ "name" : "Nerd Stuff"}' -H 'Content-Type: application/json'
```

will return

```js
{
  "error": 400,
  "message": "no type for new category provided.",
  "success": false
}
```
# <a name="delete-categories"></a>
### 8. DELETE /categories/<category_id>

Delete a Category
```bash
curl -X DELETE http://127.0.0.1:5000/categories/8
```
- Deletes specific `category` based on given id
- Request Arguments: 
  - **integer** `category_id`
- Request Headers : **None**
- Returns: 
    - **integer** `deleted` Id from deleted `category`.
    - **boolean** `success`


#### Example response
```js
{
  "deleted": 8,
  "success": true
}
```

### Errors

If you try to delete a `category` which does not exist, it will throw an `404` error:

```bash
curl -X DELETE http://127.0.0.1:5000/categories/100
```
will return
```js
{
  "error": 400,
  "message": "Category with id 100 does not exist.",
  "success": false
}
```
