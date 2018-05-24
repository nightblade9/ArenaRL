class Weapon:
    def __init__(self, owner, name, elemental = None):
        self.owner = owner
        self.name = name
        self.elemental = elemental

    def attack(self, target, game, **kwargs):
        pass
