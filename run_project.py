import logging
import os
import time

from flask import Flask, jsonify, request
from sqlalchemy.exc import OperationalError

from core import ErrorManager as Error
from core import Parser
from core.db import (
    Hero,  # noqa: F401
    User,  # noqa: F401
)
from core.db import PostgresAdapter as db_adapter
from core.db.models import database

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)


def create_app(testing=False):
    app = Flask(__name__)

    if testing:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        logging.info("App mode: testing")
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
            "DATABASE_URL", "sqlite:///:memory:"
        )
        logging.info("App mode: prod")

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    database.init_app(app)

    with app.app_context():
        for i in range(10):
            try:
                database.create_all()
                break
            except OperationalError:
                logging.warning("Database is not ready, retrying...")
                time.sleep(3)

    @app.route("/")
    def index():
        return jsonify({"msg": "Index Page"})

    @app.route("/users", methods=["GET", "POST"])
    def create_list_user_view():
        if request.method == "GET":
            users = db_adapter.get_all_users()
            return jsonify([user.as_dict() for user in users]), 200

        elif request.method == "POST":
            raw_data = request.get_json()
            user_model, error_status = Parser.user_create(raw_data)
            if error_status:
                error_msg = user_model
                logging.error(error_msg)
                return Error.Request.invalid_data_json(error_msg), 400

            user = db_adapter.create_user(user_model.username)
            hero = db_adapter.create_hero(
                user_id=user.id,
                name=user_model.hero.name,
                hp=user_model.hero.hp,
                level=user_model.hero.level,
                exp=user_model.hero.exp,
            )

            if not hero:
                logging.error(Error.DB.create_hero_error)
                return Error.DB.create_hero_error_json(), 400

            return user.as_json(), 200

    @app.route("/users/<int:user_id>", methods=["GET", "PUT", "DELETE"])
    def user_api_view(user_id):
        user = db_adapter.get_user(user_id)
        if not user:
            logging.error(Error.DB.user_not_found)
            return Error.DB.user_not_found_json(), 404

        if request.method == "GET":
            return user.as_json(), 200

        elif request.method == "PUT":
            raw_data = request.get_json()
            data = Parser.user_update(raw_data)

            if data is None:
                logging.error(Error.Request.invalid_data(raw_data))
                return Error.Request.invalid_data_json(raw_data), 400

            hero = db_adapter.update_hero(user.hero.id, **data.get("hero"))
            if not hero:
                logging.error(Error.DB.hero_not_found)
                return Error.DB.hero_not_found_json(), 404

            username = data.get("username")
            if username is not None:
                user = db_adapter.update_user(user_id, username=username)

            return user.as_json(), 200

        elif request.method == "DELETE":
            is_hero_deleted = db_adapter.delete_hero(user.hero.id)
            is_user_deleted = db_adapter.delete_user(user.id)

            return (
                jsonify(
                    {"user_deleted": is_user_deleted, "hero_deleted": is_hero_deleted}
                ),
                200,
            )

    @app.route("/users/<int:user_id>/hero", methods=["GET", "PUT", "DELETE"])
    def hero_api_view(user_id):
        user = db_adapter.get_user(user_id)
        if not user:
            logging.error(Error.DB.user_not_found)
            return Error.DB.user_not_found_json(), 404

        if request.method == "GET":
            return user.hero.as_json(), 200

        elif request.method == "PUT":
            raw_data = request.get_json()
            data = Parser.hero_update(raw_data)
            if data is None:
                logging.error(Error.Request.invalid_data(raw_data))
                return Error.Request.invalid_data_json(raw_data), 400

            hero = db_adapter.update_hero(user.hero.id, **data)
            if not hero:
                logging.error(Error.DB.hero_not_found)
                return Error.DB.hero_not_found_json(), 404

            return user.hero.as_json(), 200

        elif request.method == "DELETE":
            if db_adapter.delete_hero(user.hero.id):
                logging.info(
                    f"Hero: id={user.hero.id}, name={user.hero.name} was deleted"
                )
                return jsonify({"hero_deleted": True}), 200
            else:
                logging.error(Error.DB.hero_not_found)
                return Error.DB.hero_not_found_json(), 404

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
