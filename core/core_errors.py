

class ErrorDB:
    @staticmethod
    def user_not_found():
        return {"error": "user not found"}

    @staticmethod
    def hero_not_found():
        return {"error": "hero not found"}

    @staticmethod
    def create_hero_error():
        return {"error": "could not create hero"}


class ErrorRequest:
    @staticmethod
    def create_user_error(user_name, hero_name, hp, level, exp):
        return {
                "error": f"user_name: {user_name}, hero_name: {hero_name}, hp: {hp}, level: {level}, exp: {exp}"
            }
