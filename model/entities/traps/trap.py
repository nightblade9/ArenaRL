import colors
from game import Game
from model.components.fighter import Fighter
from model.entities.game_object import GameObject
from model.config import config

class Trap(GameObject):
    """Your basic trap. Damages whatever steps on it, and oscillates on/off."""

    def __init__(self, x, y, name='Trap', colour=colors.white):
        super().__init__(x, y, '^', name, colour, blocks=False)

        Game.instance.event_bus.bind('on_entity_move', self.on_entity_move, self)
        Game.instance.event_bus.bind('on_turn_pass', self.on_turn_passed, self)

        self._is_active = True
        self._turns_in_current_state = 0

    def on_entity_move(self, entity):
        if self._is_active and (entity.x, entity.y) == (self.x, self.y):
            self.stab(entity)
    
    def on_turn_passed(self):
        self._turns_in_current_state += 1
        if self._turns_in_current_state >= config.data.traps.oscillationTurns:
            self._is_active = not self._is_active
            self.char = "^" if self._is_active else "."
            self._turns_in_current_state = 0

    def stab(self, entity):
        fighter = Game.instance.fighter_system.get(entity)
        if fighter is not None:
            damage = config.data.traps.stepOnDamage
            fighter.take_damage(damage)
        else:
            entity.default_death_function() # I BREAK you!