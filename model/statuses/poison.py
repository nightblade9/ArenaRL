from game import Game
from model.components.base import Component
from model.config import config
from model.helper_functions.message import message

class Poison(Component):
    """Your basic poison. Inflicts config-specified damage for a number of turns."""
    def __init__(self, target):
        self.target = target
        # Poison compounds automatically.
        target.statuses.append(self)
        Game.instance.event_bus.bind('on_entity_move', self.on_entity_move, self)
        self.turns_inflicted = 0
        message(f"{target.name} is poisoned!")        

    def on_entity_move(self, who_moved):
        if who_moved == self.target:
            fighter = Game.instance.fighter_system.get(who_moved)
            if fighter is not None:
                damage = config.data.traps.poisonDamage
                fighter.take_damage(damage)
                message(f"{who_moved.name} takes poison damage!")

            self.turns_inflicted += 1
                
            if self.turns_inflicted >= config.data.traps.poisonTurns:                
                self.target.statuses.remove(self)
                Game.instance.event_bus.unregister(self)
                message(f"{self.target.name} is no longer poisoned!")