# Coffee Shop Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

You should always be working in a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized:

  ```bash
  $ cd YOUR_PROJECT_DIRECTORY_PATH/
  $ virtualenv --no-site-packages env
  $ source env/bin/activate
  ```

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. This has been precoded by Udacity since this project is alk about Idendification & Authorization. I configered it that way that in resets on every server-reset, with a preset of data.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Testing

Just like the 2nd Project, I used `Test-Driven-Development` to implement all Endpoints. 

I used `Postman Collections` to test all my Endpoints for expected behaviour & correct permission execution.

To execute the tests, follow these steps:

1. Install [Postman](https://www.getpostman.com/downloads/)
2. Download the `Postman Collection` in this Repo (`udacity-fsnd-udaspicelatte.postman_collection.json`)
3. Open `Postman` and click on "Import" on the upper-left corner
4. Select `udacity-fsnd-udaspicelatte.postman_collection.json`
5. Once uploaded, you can simple click on "Runner" (right next to "Import") and start all tests.

>_tip_: Dont forget to have **flask** running before testing!

Please note that tests have been made with (possibly) invalid tokens, so some of them won´t pass anymore.