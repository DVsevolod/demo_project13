

def parse_user_request(data):
    user_name = data.get('user_name')
    hero_name = data.get('hero_name')
    hp = data.get('hp')
    level = data.get('level')
    exp = data.get('exp')
    return user_name, hero_name, hp, level, exp


def generate_user_obj(user):
    return {
        "id": user.id,
        "user_name": user.username,
        "hero": {
            "name": user.hero.name,
            "hp": user.hero.hp,
            "level": user.hero.level,
            "exp": user.hero.exp
        }
    }


def generate_hero_object(hero):
    return {
            "name": hero.name,
            "hp": hero.hp,
            "level": hero.level,
            "exp": hero.exp
        }