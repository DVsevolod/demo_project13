from flask import jsonify
from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()


class User(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(80), nullable=False)
    hero = database.relationship("Hero", back_populates="user", uselist=False)

    def __repr__(self):
        return f"<User: {self.username}>\n<Hero: {self.hero}>"

    def as_json(self):
        return jsonify(self.as_dict())

    def as_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "hero": {
                "name": self.hero.name,
                "hp": self.hero.hp,
                "level": self.hero.level,
                "exp": self.hero.exp,
            },
        }


class Hero(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(80), nullable=False)
    hp = database.Column(database.Integer)
    level = database.Column(database.Integer)
    exp = database.Column(database.Integer)

    user_id = database.Column(
        database.Integer, database.ForeignKey("user.id"), unique=True, nullable=False
    )
    user = database.relationship("User", back_populates="hero")

    def __repr__(self):
        return f"<Hero: hp={self.hp}, level={self.level}, exp={self.exp}>"

    def as_json(self):
        return jsonify(self.as_dict())

    def as_dict(self):
        return {"name": self.name, "hp": self.hp, "level": self.level, "exp": self.exp}
