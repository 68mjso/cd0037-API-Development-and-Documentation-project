import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASS")
database_name = os.getenv("DB_NAME_TEST")


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = database_name
        self.database_path = "postgresql://{}/{}".format(
            f"{user}:{password}@{host}:{port}", self.database_name
        )

        self.app = create_app({"SQLALCHEMY_DATABASE_URI": self.database_path})
        self.client = self.app.test_client

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_default_behavior(self):
        """Test _____________"""
        res = self.client().get("/")

        self.assertEqual(res.status_code, 200)

    # /categories - GET
    def test_get_categories(self):
        response = self.client().get("/categories")
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], 200)
        self.assertTrue(data["categories"])

    def test_get_categories_wrong_method(self):
        response = self.client().post("/categories")
        self.assertEqual(response.status_code, 405)

    # /questions - GET
    def test_get_questions(self):
        response = self.client().get("/questions")
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], 200)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])
        self.assertTrue(data["current_category"])

    def test_get_questions_wrong_method(self):
        response = self.client().patch("/questions")
        self.assertEqual(response.status_code, 405)

    # /questions/<int:id> - PUT
    def test_put_questions(self):
        response = self.client().put(
            "/questions/4",
            json={"question": "test", "answer": "test", "difficulty": 1, "category": 1},
        )
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], 200)
        self.assertTrue(data["message"])

    def test_put_questions_failed(self):
        response = self.client().put("/questions/0")
        self.assertEqual(response.status_code, 404)

    # /questions/<int:id> - DELETE
    def test_delete_questions(self):
        response = self.client().delete("/questions/2")
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], 200)
        self.assertTrue(data["message"])

    def test_delete_questions_failed(self):
        response = self.client().delete("/questions/0")
        self.assertEqual(response.status_code, 404)

    # /questions - POST
    def test_post_questions(self):
        response = self.client().post(
            "/questions",
            json={"question": "test", "answer": "test", "difficulty": 1, "category": 1},
        )
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], 200)
        self.assertTrue(data["message"])

    def test_post_questions_failed(self):
        response = self.client().post(
            "/questions",
            json={},
        )
        self.assertEqual(response.status_code, 400)

    # /questions/search - POST
    def test_post_search_questions(self):
        response = self.client().post(
            "/questions/search",
            json={"searchTerm": "what"},
        )
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], 200)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["current_category"])

    def test_post_search_questions_failed(self):
        response = self.client().post(
            "/questions/search",
            json={},
        )
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["status"], 400)

    # /categories/<int:id>/questions - GET
    def test_get_categories_questions(self):
        response = self.client().get("/categories/1/questions")
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], 200)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["current_category"])

    def test_get_categories_questions_failed(self):
        response = self.client().get("/categories/0/questions")
        data = response.get_json()
        self.assertEqual(data["status"], 404)
        self.assertEqual(response.status_code, 404)

    # /quizzes - POST
    def test_post_quizzes(self):
        response = self.client().post(
            "/quizzes",
            json={"previous_questions": [], "quiz_category": {"type": "All", "id": 0}},
        )
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], 200)
        self.assertTrue(data["question"])

    def test_post_quizzes_failed(self):
        response = self.client().post(
            "/quizzes",
            json={},
        )
        self.assertEqual(response.status_code, 400)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
