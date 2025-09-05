from pydantic import ValidationError

from core.models import User


class Parser:
    @staticmethod
    def user_create(data):
        try:
            user = User(**data)
        except ValidationError as e:
            return e, True
        else:
            return user, False

    @staticmethod
    def user_update(data):
        upd_data = {}

        username = data.get("username")
        if username is not None:
            upd_data["username"] = username

        hero = Parser.hero_update(data)
        if hero is not None:
            upd_data["hero"] = hero
            return upd_data

        return

    @staticmethod
    def hero_update(data):
        upd_data = {}
        for key, val in data.items():
            if key == "name":
                upd_data[key] = val
            if key == "level":
                upd_data[key] = val
            if key == "hp":
                upd_data[key] = val
            if key == "exp":
                upd_data[key] = val

        if upd_data:
            return upd_data

        return
