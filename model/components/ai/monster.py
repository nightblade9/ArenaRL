import colors
from model.components.walkers.random_walker import RandomWalker
from model.config import config
from constants import CONFUSE_NUM_TURNS
from game import Game
from model.helper_functions.message import message
from model.components.ai.base import AbstractAI


class BasicMonster(AbstractAI):
    """
    AI for a basic monster.
    """
    def _take_turn(self):
        # a basic monster takes its turn. If you can see it, it can see you
        monster = self.owner
        if (monster.x, monster.y) in Game.instance.renderer.visible_tiles:

            # move towards player if far away
            if monster.distance_to(Game.instance.player) >= 2:
                monster.move_towards(Game.instance.player.x, Game.instance.player.y)

            # close enough, attack! (if the player is still alive.)
            elif Game.instance.fighter_system.get(Game.instance.player).hp > 0:
                Game.instance.fighter_system.get(monster).attack(Game.instance.player)

        else:
            if config.data.enemies.randomlyWalkWhenOutOfSight:
                RandomWalker(Game.instance.area_map, monster).walk()


class StunnedMonster(AbstractAI):
    """
    AI for a temporarily stunned monster (reverts to previous AI after a while).
    """
    def __init__(self, owner, num_turns=None):
        super().__init__(owner, num_turns or config.data.weapons.numTurnsStunned)

    def _take_turn(self):
        if self.num_turns > 0:  # still stunned ...
            self.num_turns -= 1
            self.owner.char = str(self.num_turns)[-1]  # last digit

        if self.num_turns == 0:
            message('The ' + self.owner.name + ' is no longer stunned!', colors.red)
            self.owner.char = self.owner.name[0]


class FrozenMonster(StunnedMonster):
    def __init__(self, owner, num_turns=None):
        super().__init__(owner, num_turns or config.data.skills.frostbomb.turnsToThaw)
        self.owner_fighter = Game.instance.fighter_system.get(owner)

        self.owner_fighter.take_damage_strategy = self.new_take_damage_strategy

    def new_take_damage_strategy(self, damage):
        if self.owner_fighter.hp <= self.owner_fighter.max_hp // 2:
            self.owner_fighter.die()
        else:
            self.owner_fighter.default_take_damage_strategy(damage)

    def cleanup(self):
        self.owner_fighter.take_damage_strategy = self.owner_fighter.default_take_damage_strategy


class ConfusedMonster(AbstractAI):
    """
    AI for a temporarily confused monster (reverts to previous AI after a while).
    """
    def __init__(self, owner, num_turns=None):
        super().__init__(owner, num_turns or CONFUSE_NUM_TURNS)
        self.walker = RandomWalker(Game.instance.area_map, owner)

    def _take_turn(self):
        if self.num_turns > 0:  # still confused...
            # move in a random direction, and decrease the number of turns confused
            self.walker.walk()
            self.num_turns -= 1

        if self.num_turns == 0:
            message('The ' + self.owner.name + ' is no longer confused!', colors.red)
