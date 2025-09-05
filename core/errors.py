from flask import jsonify


class ErrorDB:
    user_not_found = {"error": "user not found"}
    hero_not_found = {"error": "hero not found"}
    create_hero_error = {"error": "could not create hero"}

    @classmethod
    def user_not_found_json(cls):
        return jsonify(cls.user_not_found)

    @classmethod
    def hero_not_found_json(cls):
        return jsonify(cls.hero_not_found)

    @classmethod
    def create_hero_error_json(cls):
        return jsonify(cls.create_hero_error)


class ErrorRequest:
    invalid_data_obj = {"error": "invalid data: "}

    @classmethod
    def invalid_data_json(cls, data):
        cls.invalid_data_obj["error"] = list(cls.invalid_data_obj.values())[0] + str(
            data
        )
        return jsonify(cls.invalid_data_obj)

    @classmethod
    def invalid_data(cls, data):
        cls.invalid_data_obj["error"] = list(cls.invalid_data_obj.values())[0] + str(
            data
        )
        return cls.invalid_data_obj


class ErrorManager:
    DB = ErrorDB
    Request = ErrorRequest
