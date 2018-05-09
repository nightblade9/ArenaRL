from game import Game
import math
from model.rect import Rect
from model.maps.generators import map_generator


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
                print("x={}, num={}".format(x, num_vertical_walls))
                for y in range(num_vertical_walls):
                    # top-left quadrant
                    self._area_map.tiles[x][y].convert_to_wall()
                    # bottom-left quadrant
                    self._area_map.tiles[x][self._area_map.height - y - 1].convert_to_wall()
                    # top-right quadrant
                    self._area_map.tiles[self._area_map.width - x - 1][y].convert_to_wall()
                    # bottom-right quadrant
                    self._area_map.tiles[self._area_map.width - x - 1][self._area_map.height - y - 1].convert_to_wall()

        print("ADding monztesrz")
        map_generator.generate_monsters(self._area_map, Game.instance.random.randint(*ArenaGenerator.NUM_MONSTERS))