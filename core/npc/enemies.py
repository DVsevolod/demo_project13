from abc import ABC, abstractmethod


class AbstractEnemy(ABC):
    def __init__(self, name: str, hp: int, damage: int):
        self.name = name
        self.hp = hp
        self.damage = damage

    @abstractmethod
    def attack(self, target):
        pass


class Ork(AbstractEnemy):
    def attack(self, target):
        target.hp -= self.damage
