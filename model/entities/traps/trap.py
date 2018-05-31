import colors
from game import Game
from model.components.fighter import Fighter
from model.entities.game_object import GameObject
from model.config import config


class Trap(GameObject):
    """Your basic trap. Damages whatever steps on it, and oscillates on/off."""

    def __init__(self, x, y):
        super().__init__(x, y, '^', 'Fire', colors.white, blocks=False)

        Game.instance.event_bus.bind('on_entity_move', self.on_entity_move, self)
        Game.instance.event_bus.bind('on_turn_pass', self.on_turn_passed, self)

        self.is_stabbing = True
        self.turns_in_state = 0

    def on_entity_move(self, entity):
        if self.is_stabbing and (entity.x, entity.y) == (self.x, self.y):
            fighter = Game.instance.fighter_system.get(entity)
            if fighter is not None:
                damage = config.data.traps.stepOnDamage
                fighter.take_damage(damage)
            else:
                entity.default_death_function() # I BREAK you!            
    
    def on_turn_passed(self):
        self.turns_in_state += 1
        if self.turns_in_state >= config.data.traps.oscillationTurns:
            self.is_stabbing = not self.is_stabbing
            self.char = "^" if self.is_stabbing else "."
            self.turns_in_state = 0