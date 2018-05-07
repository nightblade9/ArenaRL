from game import Game
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

        # Fill with ground
        for x in range(self._area_map.width):
            for y in range(self._area_map.height):
                self._area_map.tiles[x][y].convert_to_ground()

        map_generator.generate_monsters(self._area_map, Game.instance.random.randint(*ArenaGenerator.NUM_MONSTERS))