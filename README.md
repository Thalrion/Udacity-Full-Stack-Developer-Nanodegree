# FSND Full-Stack-Developer Project Submissions

Portfolio of Projects from the Udacity-FSND.

Successor of my first Udacity Nanodegree [Intro to Programming](https://github.com/Thalrion/Udacity-Intro-to-Programming-Nanodegree).

### Project 1: Booking Site Fy-yur

est. time spent: `32 hours` (including pre-courses)

Aim of the project was to build a full-stack Web App with Flask and Boostrap which enables
Venues & Artists to list themselves and arrange Shows together.

Used tech stack:
- `SQLAlchemy` as ORM library of choice
- `PostgreSQL` as database
- `Python3` and `Flask` for server language and framework
- `Flask-Migrate` for creating and running schema migrations
- Frontend: HTML, CSS, and Javascript with Bootstrap 3 (mainly provided by Udacity Team)

Applied concepts:
- How to use Git Bash & Github as version control tool
- Configure local database and connect it to a web application
- Create Model Schemas with columns and relationships (1:1, 1:n and N:N)
- Use SQLAlchemy ORM with PostgreSQL to query, insert, edit & delete Data
- Use WTForms to encapsulate input forms in seperate file & to allow for custom validations
- Use Boostrap as a simple to use Front End Libary and Ajax to fetch flask routes
- Create SQL-like Queries, but without any SQL syntax, only using SQLAlchemy ORM
- How to clearly structurize a larger web application in different files & folders

[View Project](https://github.com/Thalrion/Udacity-Full-Stack-Developer-Nanodegree/tree/master/project01_fyyur).

### Project 2: Trivia API

est. time spent: `36 hours` (including pre-courses)

Using 'Flask' and 'React', created a Full-Stack App to manage questions
for different categories & develop an API to power the Quiz Gameplay.

Used tech stack:
- React Components as frontend (provided by Udacity Team)
- Python3 and Flask for server language and API development
- `cors` to handle access to the API
- `unittest` for automated testing of APIs
- `curl` to get responses from API
- `README.md` to document project setup & API endpoints

Applied concepts:
- using best-practice `PEP8-style` to design and structur code
- `test-driven-development (TDD)` to rapidly create highly tested & maintainable endpoints.
- directly test and make response to any endpoint out there with `curl`.
- implement `errorhandler` to format & design appropiate error messages to client
- becoming aware of the importance of extensive project documentation & testing.

[View Project](https://github.com/Thalrion/Udacity-Full-Stack-Developer-Nanodegree/tree/master/project02_triviaAPI/finished).

### Project 3: Coffee Shop (Security & Authorization)

est. time spent: `16 hours` (including pre-courses)

Using 'Flask' and 'Auth0', created a Full-Stack App to let Users
login to Site & make actions according to their Role & Permission Sets.

Used tech stack:
- `Python3` & `Flask` for server language and API development 
- `SQLAlchemy` as ORM / `Sqlite` as database
- `Ionic` to serve and build the frontend (provided by Udacity Team)
- `Auth0` as external Authorization Service & permission creation
- `jose` JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTs.
- `postman` to automatize endpoint testing & verification of correct Authorization behaviour.

[View Project](https://github.com/Thalrion/Udacity-Full-Stack-Developer-Nanodegree/tree/master/project03_coffee_shop/finished).

### Project 4: Server Deployment, Containerization and Testing

est. time spent: `24 hours` (including pre-courses)

Deployed a Flask API to a Kubernetes cluster using Docker, AWS EKS, CodePipeline, and CodeBuild.

(Application has been teared down after successfull review to avoid incurring additional costs)
[View Project](https://github.com/Thalrion/FSND-Deploy-Flask-App-to-Kubernetes-Using-EKS).

Used tech stack:
- `Docker` for app containerization & image creation to ensure environment consistency across development and production server
- `AWS EKS` & `Kubernetes` as container orchestration service to allow for horizontal scaling
- `aswscli` to interact with AWS Cloud Services
- `ekscli` for EKS cluster creation
- `kubectl` to interact with kubernetes cluster & pods
- `CodePipeline` for Continuous Delivery (CD) & to watch Github Repo for changes
- `CodeBuild` for Continuous Integration (CI), together with `pytest` for automated testing before deployment


### Project 5: Capstone

