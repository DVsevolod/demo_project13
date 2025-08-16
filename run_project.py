import os

from flask import Flask, jsonify, request

from core.db import User, Hero, PostgresAdapter as db_adapter
from core.db import database


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        "postgresql://postgres:psql_admin@localhost:5432/postgres"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    database.init_app(app)

    with app.app_context():
        database.create_all()  # create tables

    return app


app = create_app()

@app.route('/')
def index():
    return jsonify({"msg": "Index Page"})

@app.route('/users', methods=['GET', 'POST'])
def create_retrieve_user_view():
    __post_request_obj = {
        "user_name": "test_user",
        "hero_name": "Testicula",
        "hp": 100,
        "level": 0,
        "exp": 0
    }

    if request.method == 'GET':
        users = db_adapter.get_all_users()
        return jsonify([
            {
                "id": user.id,
                "username": user.username,
                "hero": {
                    "name": user.hero.name,
                    "hp": user.hero.hp,
                    "level": user.hero.level,
                    "exp": user.hero.exp
                }
            }
            for user in users
        ])
    elif request.method == 'POST':
        data = request.get_json()

        user_name = data.get('user_name')
        hero_name = data.get('hero_name')
        hp = data.get('hp')
        level = data.get('level')
        exp = data.get('exp')

        if None in [user_name, hero_name, hp, level, exp]:
            return jsonify({
                "error": f"user_name: {user_name}, hero_name: {hero_name}, hp: {hp}, level: {level}, exp: {exp}"
            })

        user = db_adapter.create_user(user_name)
        hero = db_adapter.create_hero(user_id=user.id, name=hero_name, hp=hp, level=level, exp=exp)
        if not hero:
            return jsonify({"error": "could not create hero"})
        return jsonify({
            "user": user.username,
            "hero":
                {
                    "name": hero.name,
                    "hp": hero.hp,
                    "level": hero.level,
                    "exp": hero.exp
                }
        })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
