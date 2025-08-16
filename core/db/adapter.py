from core.db.models import database, User, Hero


class PostgresAdapter:
    @staticmethod
    def create_user(username):
        user = User(username=username)
        database.session.add(user)
        database.session.commit()
        return user

    @staticmethod
    def create_hero(user_id, name, hp, level, exp):
        hero = Hero(user_id=user_id, name=name, hp=hp, level=level, exp=exp)
        database.session.add(hero)
        database.session.commit()
        return hero

    @staticmethod
    def get_user(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def get_hero(hero_id):
        return Hero.query.get(hero_id)

    @staticmethod
    def get_all_heroes():
        return Hero.query.all()

    @staticmethod
    def update_user(user_id, **kwargs):
        user = User.query.get(user_id)
        if not user:
            return None
        for key, value in kwargs.items():
            setattr(user, key, value)
        database.session.commit()
        return user

    @staticmethod
    def update_hero(hero_id, **kwargs):
        hero = Hero.query.get(hero_id)
        if not hero:
            return None
        for key, value in kwargs.items():
            setattr(hero, key, value)
        database.session.commit()
        return hero

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return False
        database.session.delete(user)
        database.session.commit()
        return True

    @staticmethod
    def delete_hero(hero_id):
        hero = Hero.query.get(hero_id)
        if not hero:
            return False
        database.session.delete(hero)
        database.session.commit()
        return True
