# Backend- Casting Agency API

This casting agency API can be used to create and manage movies and actors. You can also assign different roles to different users with different permission scopes in the company.

This API is depolyend on: https://my-casting-3366.herokuapp.com/. since it doesn't include a homepage router, you will see 404 error json. 
To see the functions and data, you need to go to the speficic endpoints.


## Pre-requisites

### Installing Dependencies

1. **Python 3.7** - Download python from this website:https://www.python.org/downloads/

2. **Virtual Environment** - Recomment using a virtual environment. Initialize and activate a virtualenv using:
```bash
python -m virtualenv env
source env/bin/activate
````

3. **Pip Dependencies** - After setting up the virtual env, install the required pacages by running:
```bash
pip install -r requirements.txt
````

### Database Setup

Setup two seperate databases: casting & casting_test(the latter one is for the testcase).

```bash
createdb casting
createdb casting_test
```

To populate the database with data, please run:

```bash
psql casting < capstone.psql
psql casting_test < capstone.psql
```

### Running the server

To run locally, please run:

```bash
export FLASK_APP=app
export FLASK_ENV=development
flask run
```

### Running the test

To run the test, run:

```bash
python test_app.py
```

## API reference

### Authentication

This project uses auth0 for login. Tokens are in the setup.sh file.

### Models:

1. Movies with attributes title and release date
2. Actors with atrributes name, age and gender

### Roles:

1. Casting Assistant

- Can view actors and moveis

2. Casting Director

- All permissions a Casting Assistant has and ...
- Add or delete an actor from the databse
- Modify actors and movies

3. Executive Producer

- All permissions a Casting Director has and ...
- Add or delete a movie from the database

### Error Handling

Errors are returned as JSON objects.

1. authentication errors in this format:
```
   {
   'code': 'authorization_header_missing',
   'description': 'Authorization header is expected.'
   }
```
2. endpoint errors in this format:
```
   {
   'success': False,
   'error': 405,
   'message': 'method not allowed',
   }
```

the API will return three error types based on how the request fails:

```bash
- 401: Unauthorized
- 400: Bad request
- 403: Forbidden
- 404: Not found
- 405: Method not allowed
- 422: Unprocessable
````

### Endpoints

Since this API has authentication, you need a token to check this endpoints. This is a token as a Executive Producer, you can use it to check all the endpoints:
```bash
token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IllSdl9LbDRwd1diSDJfMHpWLWphQyJ9.eyJpc3MiOiJodHRwczovL3UtY2FzdGluZy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjIzN2YzMjU0ODgzY2EwMDY5Y2ZhNmM0IiwiYXVkIjoiaHR0cDovL2xvY2FsaG9zdDo1MDAwIiwiaWF0IjoxNjQ4MDY3ODYzLCJleHAiOjE2NDgxNTQyNjMsImF6cCI6ImJqeW1IS2FOcDE4eFdLa1duU0tITHRlRDZkbWd0dWFvIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.aIEdkGMu5qR8t06aS*IMv7Wh4pm08e2vW0acChsywAcVTX8cyw3Cfa4K0Ouf2m2SIiSCfFCIWY0LOFIYmij8hW*-5dSZXkGESgP79K8ikNwjcQFABXqQ0qxrnc2t6huln9O1ClJBTPYMtwoqDO38Tw_ekHeFN-PJcfX6kYUa11GDdxFUaPAGqhFq52IWbrbOO0e9aWptTX3iHKHt_3eIRoTk0X31diEqqwqr2prON4H9ldZz7qV5biTw-K-6sSMvhHhxquo3lZYdsuEbAClQcY6au3wq4Y6c4ZnUPRnnuOaAAVX9ugUUtmYQE0vWcvrDHO1asSGYjdmLdwW_WoQnIQ'
````
You can use use the token in Postman, to try those endpoints.The following examples show the curl method.

1. **Get /movies**

- return the available movies on a given page. everypage has 10 items. The default page is page number one.
- curl -X GET https://my-casting-3366.herokuapp.com/movies -H 'Authorization: Bearer {token}'

```
{
    "movies": [
        {
            "id": 3,
            "release_date": "2022-0301",
            "title": "The batman"
        },
        {
            "id": 4,
            "release_date": "2021-09-04",
            "title": "King richard"
        },
        {
            "id": 5,
            "release_date": "2022-05-13",
            "title": "Downton Abbey"
        },
        {
            "id": 6,
            "release_date": "2022-02-05",
            "title": "Uncharted"
        },
        {
            "id": 7,
            "release_date": "1972-03-12",
            "title": "Godfather"
        },
        {
            "id": 8,
            "release_date": "1967-12-04",
            "title": "West side story"
        },
        {
            "id": 9,
            "release_date": "2021-09-09",
            "title": "Jackass forever"
        },
        {
            "id": 10,
            "release_date": "2021-08-07",
            "title": "Spencer"
        },
        {
            "id": 11,
            "release_date": "2021-11-23",
            "title": "Cry macho"
        },
        {
            "id": 12,
            "release_date": "2018-08-23",
            "title": "Dangle"
        }
    ],
    "success": true,
    "total_movies": 13
}
```

2. **Get /actors**

- return the available actors on a given page. everypage has 10 items. The default page is page number one.
- curl -X GET https://my-casting-3366.herokuapp.com/actors -H 'Authorization: Bearer {token}'
```
{
    "actors": [
        {
            "age": "39",
            "gender": "female",
            "id": 1,
            "name": "Scarlt Johanson"
        },
        {
            "age": "50",
            "gender": "male",
            "id": 34,
            "name": "Matt Damon"
        },
        {
            "age": "53",
            "gender": "male",
            "id": 35,
            "name": "Brad Pitt"
        },
        {
            "age": "32",
            "gender": "female",
            "id": 36,
            "name": "Anita Gold"
        },
        {
            "age": "43",
            "gender": "male",
            "id": 37,
            "name": "Morgan Spector"
        },
        {
            "age": "37",
            "gender": "female",
            "id": 38,
            "name": "Anna Wallice"
        },
        {
            "age": "31",
            "gender": "female",
            "id": 39,
            "name": "Judi Commer"
        },
        {
            "age": "46",
            "gender": "female",
            "id": 40,
            "name": "Lucy Liu"
        },
        {
            "age": "56",
            "gender": "male",
            "id": 41,
            "name": "Jack Davon"
        },
        {
            "age": "32",
            "gender": "female",
            "id": 42,
            "name": "Cliare Dust"
        }
    ],
    "success": true,
    "total_actors": 13
}
```

3. **Delete /moviess/<movie_id>**

- delete a movie using movie id.
- curl -X DELETE https://my-casting-3366.herokuapp.com/movies/4 -H "Content-Type: application/json" -H 'Authorization: Bearer {token}'
```
  {
  "success": true
  }
```
4. **Delete /actors/<actor_id>**
- delete an actor using actor id.
- curl -X DELETE https://my-casting-3366.herokuapp.com/actors/38 -H "Content-Type: application/json" -H 'Authorization: Bearer {token}'
```
  {
  "success": true
  }
```

5. **Patch /movies/<movie_id>**
- update a given movie
- curl -d '{"title":"West Side Story"}' -H "Content-Type: application/json" -H 'Authorization: Bearer {token}' -X PATCH https://my-casting-3366.herokuapp.com/movies/8
```
  {
  "success": true
  }
```
6. **Patch /actors/<actor_id>**
- update a given actor
- curl -d '{"gender":"female"}' -H "Content-Type: application/json" -H 'Authorization: Bearer {token}' -X PATCH https://my-casting-3366.herokuapp.com/actors/41
  {
  "success": true
  }

7. **Post /movies**

- add a new movie
- curl -d '{"title":"encanto", "release_date":"1998-08-31"}' -H "Content-Type: application/json" -H 'Authorization: Bearer {token}' -X POST https://my-casting-3366.herokuapp.com/movies

  {
  "success": true
  }

8. **Post /actors**

- add a new actor
- curl -d '{"name":"Maco Xeo", "age":"19", "gender":"male"}' -H "Content-Type: application/json" -H 'Authorization: Bearer {token}' -X POST https://my-casting-3366.herokuapp.com/actors
  {
  "success": true
  }
