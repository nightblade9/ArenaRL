class Weapon:
    def __init__(self, owner, elemental = None):
        self.owner = owner
        self.elemental = elemental

    def attack(self, target, game, **kwargs):
        pass
