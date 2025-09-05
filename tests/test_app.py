import json
import unittest

from core.db.models import database
from run_project import create_app


class AppTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app(testing=True)
        cls.app.config["TESTING"] = True
        cls.client = cls.app.test_client()

        with cls.app.app_context():
            database.create_all()

        cls._users__obj = [
            {
                "hero": {"exp": 0, "hp": 100, "level": 0, "name": "TestHero"},
                "id": 1,
                "username": "test_user"
            }
        ]
        cls._user__obj = {
            "hero": {"exp": 0, "hp": 100, "level": 0, "name": "TestHero"},
            "id": 1,
            "username": "test_user"
        }
        cls._user__obj_upd = {
            "hero": {"exp": 0, "hp": 100, "level": 1, "name": "Senor TestHero"},
            "id": 1,
            "username": "test_user"
        }
        cls._hero__obj = {
            "name": "TestHero",
            "hp": 100,
            "level": 0,
            "exp": 0
        }
        cls._hero__obj_upd = {
            "name": "Senor TestHero",
            "hp": 100,
            "level": 1,
            "exp": 0
        }

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            database.session.remove()
            database.drop_all()

    def test_index_route(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"msg": "Index Page"})

    def test_create_user(self):
        response = self.client.post(
            "/users",
            data=json.dumps(self._user__obj),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), self._user__obj)

    def test_get_users(self):
        response = self.client.get("/users")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), self._users__obj)

    def test_get_user(self):
        response = self.client.get("/users/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), self._user__obj)

    def test_update_user(self):
        response = self.client.put(
            "/users/1",
            data=json.dumps(
                {
                    "level": 1,
                    "name": "Senor TestHero",
                    "username": "test_user"
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), self._user__obj_upd)

    def test_get_hero(self):
        response = self.client.get("/users/1/hero")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), self._hero__obj)

    def test_update_hero(self):
        response = self.client.put(
            "/users/1/hero",
            data=json.dumps(
                {
                    "level": 1,
                    "name": "Senor TestHero"
                }
            ),
            content_type="application/json",)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), self._hero__obj_upd)


if __name__ == "__main__":
    unittest.main()
