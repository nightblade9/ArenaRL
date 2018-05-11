from attrdict import AttrDict
import colors
from game import Game
import math
from model.rect import Rect
from model.maps.generators import map_generator
from model.factories import monster_factory
from model.entities.game_object import GameObject

class ArenaGenerator:
    """
    Generates a screen-size rounded-rectangle arena, with the player randomly
    placed on either the LHS or RHS in the center.
    """

    NUM_MONSTERS = (5, 10)

    def __init__(self, area_map):
        self._area_map = area_map

    def generate(self):

        # Fill with ground, minus a 2px border.
        for x in range(self._area_map.width):
            for y in range(self._area_map.height):
                if x in (0, 1, self._area_map.width - 1, self._area_map.width - 2) or y in (0, 1, self._area_map.height - 1, self._area_map.height - 2):
                    self._area_map.tiles[x][y].convert_to_wall()
                else:
                    self._area_map.tiles[x][y].convert_to_ground()

        # Diamond walls.
        for x in range(self._area_map.width):
            num_vertical_walls = 10 - x
            if num_vertical_walls:
                for y in range(num_vertical_walls):
                    # top-left quadrant
                    self._area_map.tiles[x][y].convert_to_wall()
                    # bottom-left quadrant
                    self._area_map.tiles[x][self._area_map.height - y - 1].convert_to_wall()
                    # top-right quadrant
                    self._area_map.tiles[self._area_map.width - x - 1][y].convert_to_wall()
                    # bottom-right quadrant
                    self._area_map.tiles[self._area_map.width - x - 1][self._area_map.height - y - 1].convert_to_wall()

        # Create three pillars that are 3x3 and destructable. Not exactly centered, but close enough.
        for num_pillar in range(3):
            center_pillar_x = int(self._area_map.width / 2) + (4 * num_pillar) - 4
            center_pillar_y = int(self._area_map.height / 2)
            for x in range(center_pillar_x - 1, center_pillar_x + 2):
                for y in range(center_pillar_y - 1, center_pillar_y + 2):
                    self.make_barrel(x, y)

        # map_generator.generate_monsters(self._area_map
        # , Game.instance.random.randint(*ArenaGenerator.NUM_MONSTERS))

    def make_barrel(self, x, y):
        data = AttrDict({ "health": 1, "defense": 0, "attack": 0, "xp": 0})
        barrel = monster_factory.create_monster(data, x, y, colors.brass, "0", GameObject)
        Game.instance.ai_system.set(barrel, None)
        self._area_map.entities.append(barrel)