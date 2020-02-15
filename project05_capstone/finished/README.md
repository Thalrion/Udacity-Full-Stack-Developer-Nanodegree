### Config Auth0

#### Create an App & API

1. Login to https://manage.auth0.com/ 
2. Click on Applications Tab
3. + Create Application
4. Give it a name fitting to your project and select "Regular Web Application"
5. Go to Settings and find `domain`. Copy & paste it into config.py => auth0_config['AUTH0_DOMAIN'] (i.e. replace `"example-matthew.eu.auth0.com"`)
6. Click on API Tab 
7. Create a new API:
   1. Name: `Example`
   2. Identifier `Example`
   3. Keep Algorithm as it is

>_tip_: Give the API also a Name which fits to your project context. If in doubt, just use the same word that you named your application with.

8. Go to Settings and find `Identifier`. Copy & paste it into config.py => auth0_config['API_AUDIENCE'] (i.e. replace `"Example"`)

#### Create Roles & Permissions

In some cases, you don´t want to allow every user of your API to do the same thing.
For example, an internal dev collegue should be allowed to `POST` to your API to create new records,
while an external user should only allowd to `GET`.

With ´Auth0`, is pretty simple to do that:

1. Before creating `Roles & Permissions`, you need to `Enable RBAC` in your API (API => Click on your API Name => Settings = Enable RBAC => Save)
2. First, create a new Role under `Users and Roles` => `Roles` => `Create Roles`
3. Give it a descriptive name like `Dev Ops Guy`. Also, describe its permissions in a few words like "Can see Bookings and create them"
4. Go back to the API Tab and find your newly created API. Click on Permissions.
5. Add a new permission. Try to follow a naming convention like `action:objectnames`, (i.e. `create:bookings` or `read:properties` etc.). Also, don´t forget to add some descriptions.

>_tip_: These names are later used when you decorate your API´s, so chose them wisely! Also, always use plural names (i.e. not `create:booking`, but `create:bookings`.) Using plural names is considered best practice when designing API´s.

5. After you created all permissions your app needs, go back to `Users and Roles` => `Roles` and select the role you recently created.
6. Under `Permissions`, assign all permissions you want this role to have. 

Nice! When you set up all roles, you can simply create a new User (under the User Tab in Auth0) and assign them
an appropiate role. 

Within your API methods, decorate them with `@requires_auth('get:examples')`. Use the permission names as argument.

<a name="api-documentaton"></a>
## API Documentation

Here you can find all existing endpoints, which methods can be used, how to work with them & example responses you´ll get.

Additionally, common pitfalls & error messages are explained, if applicable.

### Base URL

Since this API is not hosted on a specific domain, it can only be accessed when
`flask` is run locally. To make requests to the API via `curl` or `postman`,
you need to use the default domain on which the flask server is running.

**_http://127.0.0.1:8080/_**

### Available Endpoints

Here is a short table about which ressources exist and which method you can use on them.

                          Allowed Methods
       Endpoints    |  GET |  POST |  DELETE | 
                    |------|-------|---------|
      /example      |  [x] |  [x]  |   [x]   |         
      /example1     |  [x] |  [x]  |   [x]   |           
      /example2     |      |  [x]  |         | 


### How to work with each endpoint

Click on a link to directly get to the ressource.

1. Example
   1. [GET /example_get_endPoint](#get-examples)

Each ressource documentation is clearly structured:
1. Description in a few words
2. `curl` example that can directly be used in terminal
3. More descriptive explanation of input & outputs.
4. Example Response.
5. Error Handling (`curl` command to trigger error + error response)

# <a name="get-examples"></a>
### 1. GET /example

Fetch example:
```bash
$ curl -X GET http://127.0.0.1:5000/exampleGetEndPoint
```
- Fetches a list of dictionaries of examples in which the keys are the ids with all available fields
- Request Arguments: 
    - **integer** `page` (optional, 10 questions per page, defaults to `1` if not given)
- Request Headers: **None**
- Returns: 
  1. List of dict of questions with following fields:
      - **integer** `id`
      - **string** `description`
  3. **boolean** `success`

#### Example response
```js
{
  "success": true
}

```
#### Errors
If you try fetch a page which does not have any examples, you will encounter an error which looks like this:

```bash
curl -X GET http://127.0.0.1:5000/exampleGetEndPoint?page=1
```

will return

```js
{
  "error": 404,
  "message": "no examples found in database.",
  "success": false
}

```