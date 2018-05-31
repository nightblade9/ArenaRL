import colors
from model.entities.traps.trap import Trap
from model.statuses.poison import Poison
from model.helper_functions.message import message

class PoisonTrap(Trap):
    def __init__(self, x, y):
        super().__init__(x, y, 'Poison Trap', colors.green)

    def stab(self, entity):
        # Called in response to on_entity_moved
        super().stab(entity)
        Poison(entity) # appends to statuses

