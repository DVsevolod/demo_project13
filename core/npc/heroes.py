from abc import ABC, abstractmethod


class AbstractHero(ABC):
    def __init__(self, name: str, hp: int, level: int):
        self.name = name
        self.hp = hp
        self.level = level
        self.exp = 0

    @abstractmethod
    def attack(self, target):
        pass

    @abstractmethod
    def use_ability(self, target):
        pass

    @property
    def _exp_threshold(self):
        return 250 * self.level**2 + 750

    def _level_up(self):
        self.level += 1
        self.hp += 10

    def add_exp(self, exp):
        self.exp += exp
        if self.exp >= self._exp_threshold:
            self.exp -= self._exp_threshold
            self._level_up()

    def is_alive(self):
        return self.hp > 0


class Revenant(AbstractHero):
    def __init__(self, name, hp=100, level=0):
        super().__init__(name, hp, level)
        self.curse = 0

    def attack(self, target):
        target.hp -= 10 + self.level
        self.curse += 5

    def use_ability(self, target):
        if self.curse >= 20:
            target.hp -= 30
            self.curse -= 20
        else:
            print('Not enough curse!')


class Bloodsmith(AbstractHero):
    def attack(self, target):
        target.hp -= 10 + self.level

    def use_ability(self, target):
        self.hp -= 15
        if self.is_alive():
            target.hp -= 25
        else:
            print('Died of blood loss')


class Soulkeeper(AbstractHero):
    def __init__(self, name, hp=100, level=0):
        super().__init__(name, hp, level)
        self.souls = 0

    def attack(self, target):
        target.hp -= 10 + self.level
        if "7" in str(target.hp):
            self.souls += 1

    def use_ability(self, target):
        if self.souls:
            target.hp -= (self.souls + 3)**2
            self.souls = 0
        else:
            print('Not enough souls!')


if __name__ == '__main__':
    bloodsmith = Soulkeeper('test-soulkeeper', hp=100, level=3)
    print(bloodsmith._exp_threshold)