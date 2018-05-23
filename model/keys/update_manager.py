from game import Game
import handicaps
import importlib
import inspect
from model.config import config
from model.event.event_bus import EventBus
from model.keys import update_manager
import random

class UpdateManager:
    def __init__(self, game):
        self.game = game

    def update(self, delta_time):
        self.base_update()
        if self.game.current_turn is self.game.player:
            pass
        else:  # it's everyone else's turn
            self.take_enemy_turns()
            self.restore_skill_points()
            self.game.event_bus.trigger('on_turn_pass')

    def take_enemy_turns(self):
        for e in self.game.area_map.entities:
            self.game.ai_system.take_turn(e)

        self.game.current_turn = self.game.player

    def restore_skill_points(self):
        skills = self.game.skill_system.get(self.game.player)
        skills.restore_skill_points(config.data.player.skillPointsPerTurn)

    def base_update(self):
        if self.game.renderer.recompute_fov:
            go_to_next_floor = ((self.game.player.x, self.game.player.y) == self.game.area_map.next_floor_stairs)
            go_to_previous_floor = ((self.game.player.x, self.game.player.y) == self.game.area_map.previous_floor_stairs)
            
            if go_to_next_floor or go_to_previous_floor:
                self.switch_floor(go_to_next_floor)
        self.game.renderer.render()

    def switch_floor(self, go_to_next_floor):
        self.game.area_map.entities = []        
        update_manager.generate_floor()
        self.game.event_bus = EventBus()
        # TODO: this is handled case-by-case by the dungeon generator; arena generator
        # sets this but other generators don't. Come up with a more generic way to handle this.
        #self.place_player_in_floor(self.game.area_map.next_floor_stairs)
        if go_to_next_floor and config.data.features.handicapOnFloorDescend:
            # ya'ne, not going to the previous floor
            # Pick a random method from the handicaps module. Call it with player as an arg.
            # That's the handicap that we're applying this floor.
            handicap_methods = [x for x in inspect.getmembers(handicaps) if inspect.isfunction(x[1])]
            handicap_method_names = [x[0] for x in handicap_methods]
            random.shuffle(handicap_method_names)
            
            handicap_method = getattr(handicaps, handicap_method_names.pop())
            handicap_method(Game.instance.player)

        self.refresh_renderer()

    def place_player_in_floor(self, tile_to_spawn_player_around):
        self.game.area_map.place_around(self.game.player, *tile_to_spawn_player_around)
        if config.data.stallion.enabled:
            if self.game.stallion.is_mounted:
                self.game.area_map.entities.append(self.game.stallion)
                self.game.stallion.x, self.game.stallion.y = self.game.player.x, self.game.player.y
            else:
                self.game.area_map.place_around(self.game.stallion, self.game.player.x, self.game.player.y)

    def refresh_renderer(self):
        self.game.renderer.reset()
        self.game.renderer.refresh_all()

def generate_floor():
    # generate map (at this point it's not drawn to the screen)
    generator_class_name = f'{str(config.data.mapType).lower().capitalize()}Generator'
    module_name = 'model.maps.generators.{}_generator'.format(config.data.mapType).lower()
    module = importlib.import_module(module_name)
    generator = getattr(module, generator_class_name)
    generator(Game.instance.area_map).generate()