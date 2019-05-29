"""
from abc import ABC, abstractmethod


class Hero:
    def __init__(self):
        self.positive_effects = []
        self.negative_effects = []

        self.stats = {
            "HP": 128,
            "MP": 42,
            "SP": 100,

            "Strength": 15,
            "Perception": 4,
            "Endurance": 8,
            "Charisma": 2,
            "Intelligence": 3,
            "Agility": 8,
            "Luck": 1
        }

    def get_positive_effects(self):
        return self.positive_effects.copy()

    def get_negative_effects(self):
        return self.negative_effects.copy()

    def get_stats(self):
        return self.stats.copy()
"""

class AbstractEffect(Hero, ABC):
    def __init__(self, base):
        Hero.__init__(self)
        self.base = base

    @abstractmethod
    def get_stats():
        pass

    @abstractmethod
    def get_positive_effects():
        pass

    @abstractmethod
    def get_negative_effects():
        pass


class AbstractPositive(AbstractEffect):
    pass


class AbstractNegative(AbstractEffect):
    pass


class Berserk(AbstractPositive):
    def get_stats(self):
        self.stats = self.base.get_stats()
        for key in ("Strength", "Endurance", "Agility", "Luck"):
            self.stats[key] += 7
        for key in ("Perception", "Charisma", "Intelligence"):
            self.stats[key] -= 3
        self.stats['HP'] += 50
        return self.stats.copy()

    def get_positive_effects(self):
        self.positive_effects = self.base.get_positive_effects()
        self.positive_effects.append("Berserk")
        return self.positive_effects.copy()

    def get_negative_effects(self):
        return self.base.get_negative_effects()


class Blessing(AbstractPositive):
    def get_stats(self):
        self.stats = self.base.get_stats()
        for key in ("Strength", "Endurance", "Agility", "Luck", "Perception", "Charisma", "Intelligence"):
            self.stats[key] += 2
        return self.stats.copy()

    def get_positive_effects(self):
        self.positive_effects = self.base.get_positive_effects()
        self.positive_effects.append("Blessing")
        return self.positive_effects.copy()

    def get_negative_effects(self):
        return self.base.get_negative_effects()


class Weakness(AbstractNegative):
    def get_stats(self):
        self.stats = self.base.get_stats()
        for key in ("Strength", "Endurance", "Agility"):
            self.stats[key] -= 4
        return self.stats.copy()

    def get_negative_effects(self):
        self.negative_effects = self.base.get_negative_effects()
        self.negative_effects.append("Weakness")
        return self.negative_effects.copy()

    def get_positive_effects(self):
        return self.base.get_positive_effects()


class EvilEye(AbstractNegative):
    def get_stats(self):
        self.stats = self.base.get_stats()
        self.stats["Luck"] -= 10
        return self.stats.copy()

    def get_negative_effects(self):
        self.negative_effects = self.base.get_negative_effects()
        self.negative_effects.append("EvilEye")
        return self.negative_effects.copy()

    def get_positive_effects(self):
        return self.base.get_positive_effects()


class Curse(AbstractNegative):
    def get_stats(self):
        self.stats = self.base.get_stats()
        for key in ("Strength", "Endurance", "Agility", "Luck", "Perception", "Charisma", "Intelligence"):
            self.stats[key] -= 2
        return self.stats.copy()

    def get_negative_effects(self):
        self.negative_effects = self.base.get_negative_effects()
        self.negative_effects.append("Curse")
        return self.negative_effects.copy()

    def get_positive_effects(self):
        return self.base.get_positive_effects()
