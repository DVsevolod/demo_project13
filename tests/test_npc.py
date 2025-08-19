import unittest

from core import Bloodsmith, Ork, Revenant, Soulkeeper


class TestNPC(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.abc_hero = Bloodsmith("test-abc-hero", hp=100, level=1)
        cls.bloodsmith = Bloodsmith("test-bloodsmith", hp=130, level=2)
        cls.revenant = Revenant("test-revenant", hp=100, level=3)
        cls.soulkeeper = Soulkeeper("test-soulkeeper", hp=100, level=3)

    def setUp(self):
        self.enemy = Ork("Filthy Grook", hp=50, damage=30)

    def test_base_npc_functions(self):
        self.assertEqual(self.abc_hero.hp, 100)
        self.assertEqual(self.abc_hero.level, 1)
        self.assertTrue(self.abc_hero.is_alive())

        self.abc_hero.add_exp(500)
        self.assertEqual(self.abc_hero.exp, 500)

        self.abc_hero.add_exp(1000)
        self.assertEqual(self.abc_hero.level, 2)
        self.assertEqual(self.abc_hero.exp, 500)
        self.assertEqual(self.abc_hero._exp_threshold, 1750)

        self.abc_hero._level_up()
        self.assertEqual(self.abc_hero.level, 3)
        self.assertEqual(self.abc_hero.hp, 120)
        self.assertEqual(self.abc_hero._exp_threshold, 3000)

        self.abc_hero.hp -= 1000
        self.assertFalse(self.abc_hero.is_alive())

    def test_npc_enemy(self):
        self.abc_hero.hp = 100
        self.enemy.attack(self.abc_hero)
        self.assertEqual(self.abc_hero.hp, 70)

    def test_npc_bloodsmith(self):
        self.bloodsmith.attack(self.enemy)
        self.assertEqual(self.enemy.hp, 38)

        self.bloodsmith.use_ability(self.enemy)
        self.assertEqual(self.bloodsmith.hp, 115)
        self.assertEqual(self.enemy.hp, 13)

    def test_npc_revenant(self):
        self.revenant.attack(self.enemy)
        self.assertEqual(self.enemy.hp, 37)
        self.assertEqual(self.revenant.curse, 5)

        self.revenant.curse += 25
        self.revenant.use_ability(self.enemy)
        self.assertEqual(self.revenant.curse, 10)
        self.assertEqual(self.enemy.hp, 7)

    def test_npc_soulkeeper(self):
        self.soulkeeper.attack(self.enemy)
        self.assertEqual(self.enemy.hp, 37)
        self.assertEqual(self.soulkeeper.souls, 1)

        self.soulkeeper.use_ability(self.enemy)
        self.assertEqual(self.soulkeeper.souls, 0)
        self.assertEqual(self.enemy.hp, 21)


if __name__ == "__main__":
    unittest.main()
