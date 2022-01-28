import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # test GET requests for questions

    def test_retrieve_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(len(data['categories']))
        self.assertEqual(data['currentCategory'], None)

    def test_404_requesting_beyond_page(self):
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')

    # test DELETE a question using question ID
    def test_delete_question(self):
        res = self.client().delete('/questions/12')
        data = json.loads(res.data)

        item = Question.query.filter(Question.id == 12).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_question_does_not_exist(self):
        res = self.client().delete('/questions/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # test POST a new question
    def test_create_question(self):
        res = self.client().post(
            '/questions',
            json={
                "question": "the greatest showman",
                "answer": "Hugh Jackman",
                "category": "5",
                "difficulty": 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_405_create_not_allowed(self):
        res = self.client().post(
            '/questions/1',
            json={
                "question": "the greatest showman",
                "answer": "Hugh Jackman",
                "category": "5",
                "difficulty": 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    # test get questions based on a search term
    def test_search_questions_with_results(self):
        res = self.client().post(
            '/questions/search',
            json={
                "searchTerm": "movie"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 1)
        self.assertTrue(data['totalQuestions'])
        self.assertEqual(data['currentCategory'], None)

    def test_search_questions_no_results(self):
        res = self.client().post(
            '/questions/search',
            json={
                "searchTerm": "fyyur"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['totalQuestions'], 0)
        self.assertEqual(data['currentCategory'], None)

    # test get questions based on category
    def test_get__by_category(self):
        res = self.client().get('/categories/3/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 3)
        self.assertTrue(data['totalQuestions'])
        self.assertEqual(data['currentCategory'], 'Geography')

    def test_404_get__by_category(self):
        res = self.client().get('/categories/8/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')

    # test get questions to play the quiz
    def test_play_quizzes(self):
        res = self.client().post(
            '/quizzes',
            json={
                "previous_questions": [2],
                "quiz_category": {
                    "type": "Geography",
                    "id": "2"}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
