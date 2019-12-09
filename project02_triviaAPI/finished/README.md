Full Stack Trivia API "Udacitrivia"
-----

### Introduction

Udacitrivia is a Full-Stack Web Application with following features:

1) Display questions - both all questions and by category. Questions show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

### Motiviation

Main goal and motivation of the project is to learn how to design & develop an API which
can be consumed by a seperat frontend and also from other, authorised sources.

Every line of code was implemented with `Test-Driven-Development` in mind. Before a new Endpoint was
created, I formulated and designed `Unit Tests` to check expected behaviour for successful and for bad requests.

After all tests have been written, endpoints were implemented to pass exactly these tests.

Development approach:
1. Write & formulate test (= really think about desired outcomes and stuff that could go wrong)
2. Fail test
3. Write code 
4. Pass test (?)
5. Refactor

### Main Files: Project Structure

  ```sh
  ├── README.md
  ├── backend *** Contains API and test suit. 
  │   ├── README.md *** Contains backend server setup and API documentation
  │   ├── config.py *** Contains information for database connection
  │   ├── models.py
  │   ├── flaskr
  │   │   └── __init__.py *** App creation & API endpoints.
  │   ├── requirements.txt *** The dependencies to be installed with "pip3 install -r requirements.txt"
  │   └── test_flaskr.py *** 22 unittests to check expected behaviour from API
  │   └── trivia.psql *** database dumb, restore with "psql trivia < trivia.psql"
  └── frontend *** start frontend with "npm start"
      ├── README.md *** Contains Frontend Setup 
      └── src
          └── components *** Contains React Components
  ```

### Setup Project locally

To start the project locally, you need to setup both `backend` and `frontend` seperatly.
I suggest to start with the `backend` setup, because the `React-App` consumes the data from the `flask server`. 

1. [`./frontend/`](./frontend/README.md)
2. [`./backend/`](./backend/README.md)
