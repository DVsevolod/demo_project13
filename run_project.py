import time
import os

from flask import Flask, jsonify, request
from sqlalchemy.exc import OperationalError

from core import ErrorDB, ErrorRequest, parse_user_request, generate_user_obj, generate_hero_object
from core.db import User, Hero, PostgresAdapter as db_adapter
from core.db.models import database


def create_app(testing=False):
    app = Flask(__name__)

    if testing:
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
            'DATABASE_URL',
            "postgresql://postgres:psql_admin@localhost:5432/postgres"
        )

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    database.init_app(app)

    with app.app_context():
        for i in range(10):
            try:
                database.create_all()
                break
            except OperationalError:
                print("Database not ready, retrying...")
                time.sleep(3)

    @app.route('/')
    def index():
        return jsonify({"msg": "Index Page"})

    @app.route('/users', methods=['GET', 'POST'])
    def create_list_user_view():
        if request.method == 'GET':
            users = db_adapter.get_all_users()
            return jsonify([
                generate_user_obj(user)
                for user in users
            ]), 200

        elif request.method == 'POST':
            username, hero_name, hp, level, exp = parse_user_request(request.get_json())
            if None in [username, hero_name, hp, level, exp]:
                return jsonify(ErrorRequest.create_user_error(username, hero_name, hp, level, exp)), 400

            user = db_adapter.create_user(username)
            hero = db_adapter.create_hero(user_id=user.id, name=hero_name, hp=hp, level=level, exp=exp)
            if not hero:
                return jsonify(ErrorDB.create_hero_error()), 400
            return jsonify(generate_user_obj(user)), 200

    @app.route("/users/<int:user_id>", methods=['GET', 'PUT', 'DELETE'])
    def user_api_view(user_id):
        if request.method == 'GET':
            user = db_adapter.get_user(user_id)
            if not user:
                return jsonify(ErrorDB.user_not_found()), 404

            return jsonify(generate_user_obj(user)), 200

        elif request.method == 'PUT':
            data = request.get_json()
            username = data.pop('username')
            if username is not None:
                user = db_adapter.update_user(user_id, username=username)
                if not user:
                    return jsonify(ErrorDB.user_not_found()), 404

            user = db_adapter.get_user(user_id)
            if not user:
                return jsonify(ErrorDB.user_not_found()), 404

            hero = db_adapter.update_hero(user.hero.id, **data)
            if not hero:
                return jsonify(ErrorDB.hero_not_found()), 404

            return jsonify(generate_user_obj(user)), 200

        elif request.method == 'DELETE':
            user = db_adapter.get_user(user_id)
            if not user:
                return jsonify(ErrorDB.user_not_found()), 404

            is_hero_deleted = db_adapter.delete_hero(user.hero.id)
            is_user_deleted = db_adapter.delete_user(user.id)

            return jsonify({"user_deleted": is_user_deleted, "hero_deleted": is_hero_deleted}), 200

    @app.route("/users/<int:user_id>/hero", methods=['GET', 'PUT', 'DELETE'])
    def hero_api_view(user_id):
        if request.method == 'GET':
            user = db_adapter.get_user(user_id)
            if not user:
                return jsonify(ErrorDB.user_not_found()), 404

            return jsonify(generate_hero_object(user.hero)), 200
        elif request.method == 'PUT':
            user = db_adapter.get_user(user_id)
            if not user:
                return jsonify(ErrorDB.user_not_found()), 404

            hero = db_adapter.update_hero(user.hero.id, **request.get_json())
            if not hero:
                return jsonify(ErrorDB.hero_not_found()), 404

            return jsonify(generate_hero_object(user.hero)), 200

        elif request.method == 'DELETE':
            user = db_adapter.get_user(user_id)
            if not user:
                return jsonify(ErrorDB.user_not_found()), 404

            if db_adapter.delete_hero(user.hero.id):
                return jsonify({"success": f"deleted hero: id={user.hero.id}, name={user.hero.name}"}), 200
            else:
                return jsonify(ErrorDB.hero_not_found()), 404

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
