# The trivia API of Udacity
You can use this API to manage a trivia app and play the trivia quiz game. Each question has the question itself, answer, category and difficulty rating. You can create new trivia question, delete questions, search questions and most of all, they can play the quiz either with or without a specific category.


## Pre-requisites
Developers should have python 3.7, pip and node installled on local machines.
  ### backend
  From the backend folder run pip install requirements.txt. To run the application, run the following commands:
  
     export FLASK_APP=flaskr 
     export FLASK_ENV=development
     flask run
     
  The application is run on http://127.0.0.1:5000/ by default.

  ### frontend
  From the frontend folder run the follwing commands:
  
    npm install //only once to install dependencies
    npm start 
    
  The frontend is run on http://localhost:3000/ by default.

  ### Database
  With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
  
    psql trivia < trivia.psql

  ### Testing
  To run the tests, run:
  
    dropdb trivia_test
    createdb trivia_test
    psql trivia_test < trivia.psql
    python test_flaskr.py

## API reference
  ### Authentication: N/A
  ### Error Handling
  Errors are returned as JSON objects:
  
    {
      "success": False, 
      "error": 404,
      "message": "not found"
    } 

  The API will return threee error types when requests fail:
  
    404:not found
    
    405:method not allowed
    
    422:unprocessable

  ### Endpoints
  1. **GET /categories**

  [General]: Returns all available categories.
  
  [Sample] curl http://127.0.0.1:5000/categories

    {
    "categories": {
      "1": "Science", 
      "2": "Art", 
      "3": "Geography", 
      "4": "History", 
      "5": "Entertainment", 
      "6": "Sports"
    }, 
    "success": true
    } 

  2. **GET /questions**
 
  [General]: Returns a list of questions, number of total questions, current category, categories. Results are paginated in group of 10.
  
  [Sample] curl http://127.0.0.1:5000/questions
  
    {
    "categories": {
      "1": "Science", 
      "2": "Art", 
      "3": "Geography", 
      "4": "History", 
      "5": "Entertainment", 
      "6": "Sports"
    }, 
    "currentCategory": null, 
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
      {
        "answer": "Maya Angelou", 
        "category": 4, 
        "difficulty": 2, 
        "id": 5, 
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
      }, 
      {
        "answer": "Edward Scissorhands", 
        "category": 5, 
        "difficulty": 3, 
        "id": 6, 
        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
      }, 
      {
        "answer": "Muhammad Ali", 
        "category": 4, 
        "difficulty": 1, 
        "id": 9, 
        "question": "What boxer's original name is Cassius Clay?"
      }, 
      {
        "answer": "Brazil", 
        "category": 6, 
        "difficulty": 3, 
        "id": 10, 
        "question": "Which is the only team to play in every soccer World Cup tournament?"
      }, 
      {
        "answer": "Uruguay", 
        "category": 6, 
        "difficulty": 4, 
        "id": 11, 
        "question": "Which country won the first ever soccer World Cup in 1930?"
      }, 
      {
        "answer": "George Washington Carver", 
        "category": 4, 
        "difficulty": 2, 
        "id": 12, 
        "question": "Who invented Peanut Butter?"
      }, 
      {
        "answer": "Lake Victoria", 
        "category": 3, 
        "difficulty": 2, 
        "id": 13, 
        "question": "What is the largest lake in Africa?"
      }, 
      {
        "answer": "The Palace of Versailles", 
        "category": 3, 
        "difficulty": 3, 
        "id": 14, 
        "question": "In which royal palace would you find the Hall of Mirrors?"
      }
    ], 
    "success": true, 
    "totalQuestions": 19
    }
   
  3. **DELETE /questions/{question_id}**
  
  [General]: Deletes question using a question ID.
  
  [Sample] curl http://127.0.0.1:5000/questions/23
  
    {
    "success": true
    }

   4. **POST /questions**
 
   [General]: Adds a new question. It will take in four parameters, the question, answer text, 
  category, and difficulty score.

   [Sample] curl -d '{"question":"the greatest showman", "answer":"Hugh Jackman", "category":"5", "difficulty":1}' -H "Content-Type: application/json" -X POST  http://localhost:5000/questions
    
    {
    "success": true
    }

   5. **POST /questions/search**
  
   [General]: Gets questions based on a search term, any question that has the substring of the search term will be returned.
   
   [Sample_has_results] curl -d '{"searchTerm":"the"}' -H "Content-Type: application/json" -X POST  http://localhost:5000/questions/search
   
    {
    "currentCategory": null, 
    "questions": [
      {
        "answer": "Maya Angelou", 
        "category": 4, 
        "difficulty": 2, 
        "id": 5, 
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
      }, 
      {
        "answer": "Tom Cruise", 
        "category": 5, 
        "difficulty": 4, 
        "id": 4, 
        "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
      }, 
      {
        "answer": "Edward Scissorhands", 
        "category": 5, 
        "difficulty": 3, 
        "id": 6, 
        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
      }, 
      {
        "answer": "Brazil", 
        "category": 6, 
        "difficulty": 3, 
        "id": 10, 
        "question": "Which is the only team to play in every soccer World Cup tournament?"
      }, 
      {
        "answer": "Uruguay", 
        "category": 6, 
        "difficulty": 4, 
        "id": 11, 
        "question": "Which country won the first ever soccer World Cup in 1930?"
      }, 
      {
        "answer": "Lake Victoria", 
        "category": 3, 
        "difficulty": 2, 
        "id": 13, 
        "question": "What is the largest lake in Africa?"
      }, 
      {
        "answer": "The Palace of Versailles", 
        "category": 3, 
        "difficulty": 3, 
        "id": 14, 
        "question": "In which royal palace would you find the Hall of Mirrors?"
      }, 
      {
        "answer": "Agra", 
        "category": 3, 
        "difficulty": 2, 
        "id": 15, 
        "question": "The Taj Mahal is located in which Indian city?"
      }, 
      {
        "answer": "The Liver", 
        "category": 1, 
        "difficulty": 4, 
        "id": 20, 
        "question": "What is the heaviest organ in the human body?"
      }, 
      {
        "answer": "Blood", 
        "category": 1, 
        "difficulty": 4, 
        "id": 22, 
        "question": "Hematology is a branch of medicine involving the study of what?"
      }
    ], 
    "success": true, 
    "totalQuestions": 11
    }
    
  [Sample_no_result] curl -d '{"searchTerm":"fyyur"}' -H "Content-Type: application/json" -X POST  http://localhost:5000/questions/search
  
    {
    "currentCategory": null, 
    "questions": [], 
    "success": true, 
    "totalQuestions": 0
    }

  6. **GET /categories/{category_id}/questions**
  
  [General]: Gets questions within a given category, based on a given category ID.
  
  [Sample] curl http://localhost:5000/categories/3/questions
  
    {
    "currentCategory": "Geography", 
    "questions": [
      {
        "answer": "Lake Victoria", 
        "category": 3, 
        "difficulty": 2, 
        "id": 13, 
        "question": "What is the largest lake in Africa?"
      }, 
      {
        "answer": "The Palace of Versailles", 
        "category": 3, 
        "difficulty": 3, 
        "id": 14, 
        "question": "In which royal palace would you find the Hall of Mirrors?"
      }, 
      {
        "answer": "Agra", 
        "category": 3, 
        "difficulty": 2, 
        "id": 15, 
        "question": "The Taj Mahal is located in which Indian city?"
      }
    ], 
    "success": true, 
    "totalQuestions": 3
    }

  7. **POST /quizzes**
  
  [General] Gets questions to play the quiz. It takes in two parameters, previous questions and quiz category. Previous questions is an array of the previous questions' ID. Quiz category is an object of a category, this parameter is optional.
  
  [Sample] curl -d '{"previous_questions": [2],"quiz_category": {"type":"Geography","id": "2"}}' -H 'Content-Type: application/json' -X POST http://127.0.0.1:5000/quizzes
  
      {
      "question": {
        "answer": "Escher", 
        "category": 2, 
        "difficulty": 1, 
        "id": 16, 
        "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
      }, 
      "success": true
      }

## Deployment N/A

## Authors
  Suwei Liang

## Acknowledgements
Very much thanks to this part's coach: Caryn.



----------------------------------------------------




# Full Stack API Final Project

## Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the [project repository](https://github.com/udacity/FSND/blob/master/projects/02_trivia_api/starter) and [Clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom.
>Once you're ready, you can submit your project on the last page.

## About the Stack

We started the full stack application for you. It is designed with some key functional areas:

### Backend
The [./backend](https://github.com/udacity/FSND/blob/master/projects/02_trivia_api/starter/backend/README.md) directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in `__init__.py` to define your endpoints and can reference models.py for DB and SQLAlchemy setup. These are the files you'd want to edit in the backend:

1. *./backend/flaskr/`__init__.py`*
2. *./backend/test_flaskr.py*


### Frontend

The [./frontend](https://github.com/udacity/FSND/blob/master/projects/02_trivia_api/starter/frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. If you have prior experience building a frontend application, you should feel free to edit the endpoints as you see fit for the backend you design. If you do not have prior experience building a frontend application, you should read through the frontend code before starting and make notes regarding:

1. What are the end points and HTTP methods the frontend is expecting to consume?
2. How are the requests from the frontend formatted? Are they expecting certain parameters or payloads? 

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. The places where you may change the frontend behavior, and where you should be looking for the above information, are marked with `TODO`. These are the files you'd want to edit in the frontend:

1. *./frontend/src/components/QuestionView.js*
2. *./frontend/src/components/FormView.js*
3. *./frontend/src/components/QuizView.js*


By making notes ahead of time, you will practice the core skill of being able to read and understand code and will have a simple plan to follow to build out the endpoints of your backend API. 



>View the [README within ./frontend for more details.](./frontend/README.md)
