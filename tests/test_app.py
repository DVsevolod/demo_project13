import json
import unittest

from run_project import create_app
from core.db.models import database


class AppTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app(testing=True)
        cls.client = cls.app.test_client()

        with cls.app.app_context():
            database.create_all()

        cls._users__get = [
            {
                "hero": {
                    "exp": 0,
                    "hp": 100,
                    "level": 0,
                    "name": "TestHero"
                },
                "id": 1,
                "user_name": "test_user"
            }
        ]
        cls._users__post = {
            "user_name": "test_user",
            "hero_name": "TestHero",
            "hp": 100,
            "level": 0,
            "exp": 0
        }
        cls._user__get = {
            "hero": {
                "exp": 0,
                "hp": 100,
                "level": 0,
                "name": "TestHero"
            },
            "id": 1,
            "user_name": "test_user"
        }
        cls._user__put = {
            "hero": {
                "exp": 0,
                "hp": 100,
                "level": 1,
                "name": "Senor TestHero"
            },
            "id": 1,
            "user_name": "test_user"
        }
        cls._user__delete = {
            "user_deleted": True,
            "hero_deleted": True
        }

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            database.session.remove()
            database.drop_all()

    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"msg": "Index Page"})

    def test_create_user(self):
        response = self.client.post(
            '/users',
            data=json.dumps(self._users__post),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), self._user__get)

    def test_get_users(self):
        __test__get_response_obj = [
            {
                "hero": {
                    "exp": 0,
                    "hp": 100,
                    "level": 0,
                    "name": "TestHero"
                },
                "id": 1,
                "username": "test_user"
            }
        ]

        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), self._users__get)

    def test_get_user(self):
        response = self.client.get('/users/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), self._user__get)

    def test_update_user(self):
        response = self.client.put(
            '/users/1',
            data=json.dumps({
                "user_name": "test_user",
                "name": "Senor TestHero",
                "level": 1
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), self._user__put)


if __name__ == "__main__":
    unittest.main()
