from attrdict import AttrDict
import colors
from elements import Element
from game import Game
import math
from model.rect import Rect
from model.maps.generators import map_generator
from model.factories import monster_factory
from model.entities.game_object import GameObject
import random

class ArenaGenerator:
    """
    Generates a screen-size rounded-rectangle arena, with the player randomly
    placed on either the LHS or RHS in the center.
    """

    CLUSTER_SIZE = (5, 7)
    NUM_CLUSTERS = (1, 2) # 1-2 clusters of 5-7 monsters

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
                    self._make_barrel(x, y)        
        
        self._generate_stairs() # also places player
        #self._generate_monsters()

    def _generate_stairs(self):
        # Edge case: if floor num = 1, set player X/Y. Otherwise, it's set in main.py
        if self._area_map.floor_num == 1:
            Game.instance.player.y = int(Game.instance.area_map.height / 2)
            Game.instance.player.x = 5 if random.choice(['left', 'right']) == 'left' else Game.instance.area_map.width - 5        

        stairs_x = self._area_map.width - Game.instance.player.x
        stairs_y = Game.instance.player.y
        stairs_tile = self._area_map.tiles[stairs_x][stairs_y]
        stairs_tile.convert_to_ground(character='>', colour=colors.white, dark_colour=colors.grey)
        self._area_map.next_floor_stairs = (stairs_x, stairs_y)

    def _generate_monsters(self):
        # Monster generation is complicated. To keep it simple, we have a pool of generic monsters,
        # we pick two of those each round, and up their stats to be appropriate for the current floor.
        # We also generate a boss, which is a different randomly-picked monster, tanked up to 10x.
        
        # Well, technically, we just need names. They're functionally all the same.
        monster_names = ["slime", "locust", "giant", "wolf", "anaconda", "venomspider", "dragon", "thief", "hippogryph"]
        # generic colours for non-element beasties.
        monster_colours = [colors.orange, colors.purple, colors.violet, colors.pink, colors.magenta, colors.amber]
        elemental_colours = {
            Element.FIRE: colors.red,
            Element.ICE: colors.blue,
            Element.LIGHTNING: colors.yellow,
            Element.EARTH: colors.green
        }

        elements = [e for e in elemental_colours]
        random.shuffle(elements)

        num_clusters = Game.instance.random.randint(*ArenaGenerator.NUM_CLUSTERS)
        monsters = random.sample(monster_names, num_clusters + 1) # +1 = boss
        colours = random.sample(monster_colours, num_clusters + 1)

        for cluster_number in range(num_clusters):

            is_elemental = random.choice([True, False]) == True            
            num_monsters = Game.instance.random.randint(*ArenaGenerator.CLUSTER_SIZE)
            monster_name = monsters.pop()
            difficulty = (cluster_number + 1) * self._area_map.floor_num
            
            attack = random.randint(difficulty * 2, difficulty * 5)
            defense = random.randint(difficulty, difficulty * 7)
            health = random.randint(12 * difficulty, 45 * difficulty)
            colour = colours.pop()

            element = elements.pop() if is_elemental else None

            for j in range(num_monsters):
                self._create_monster(monster_name, colour, attack, defense, health, element, elemental_colours)
            
        # Boss is always someone to kill, so he should have very narrowly-ranged stats
        # TODO: what if he spawns next to you? Erm, well, you die, I guess.
        is_elemental = random.choice([True, False]) == True
        element = elements.pop() if is_elemental else None
        
        self._create_monster(monsters.pop().capitalize(), colours.pop(), difficulty * 6, difficulty * 4, difficulty * 100, element, elemental_colours)

    def _create_monster(self, monster_name, colour, attack, defense, health, element, elemental_colours):
        data = AttrDict({ 
            "attack": attack,
            "defense": defense,
            "health": health,
            "xp": (attack + defense) * health
        })

        x, y = self._area_map.get_random_walkable_tile() # TODO: place away from player's side? Nah.
        final_colour = elemental_colours[element] if element is not None else colour
        final_name = f"{element} {monster_name}" if element is not None else monster_name
        monster = monster_factory.create_monster(data, x, y, final_colour, final_name, character=monster_name[0])
        monster.elemental = element
        self._area_map.entities.append(monster)        

    def _make_barrel(self, x, y):
        data = AttrDict({ "health": 1, "defense": 0, "attack": 0, "xp": 0})
        barrel = monster_factory.create_monster(data, x, y, colors.brass, "Barrel", "0", GameObject)
        Game.instance.ai_system.set(barrel, None)
        self._area_map.entities.append(barrel)
