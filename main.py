#!/usr/bin/env python3
from random import Random
from datetime import datetime

from tcod import image_load

from model.config import file_watcher, config
file_watcher.watch('config.json', lambda raw_json: config.load(raw_json))

import colors
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, MAP_WIDTH, MAP_HEIGHT, PANEL_HEIGHT, LIMIT_FPS
from game import Game
from data.save_manager import SaveManager
from model.helper_functions.menu import create_menu, message_box
from model.helper_functions.message import message
from model.entities.party.player import Player
from model.entities.party.stallion import Stallion
from model.event.event_bus import EventBus
from model.key_binder import KeyBinder
from model.maps import generators
from model.maps.area_map import AreaMap
from model.maps.generators import ForestGenerator
from model.systems.ai_system import AISystem
from model.systems.system import ComponentSystem
from view.adapter.tdl_adapter import TdlAdapter
from view.map_renderer import MapRenderer


def new_game():

    Game.instance.fighter_system = ComponentSystem()
    Game.instance.xp_system = ComponentSystem()
    Game.instance.skill_system = ComponentSystem()
    Game.instance.ai_system = AISystem()

    Game.instance.player = Player()
    if config.data.stallion.enabled:
        Game.instance.stallion = Stallion(Game.instance.player)

    for i in range(1, config.data.numFloors + 1):
        Game.instance.area_map = AreaMap(MAP_WIDTH, MAP_HEIGHT, i)
        Game.instance.event_bus = EventBus()

        # generate map (at this point it's not drawn to the screen)
        generator_class_name = f'{str(config.data.mapType).lower().capitalize()}Generator'
        generator = getattr(generators, generator_class_name, ForestGenerator)
        generator(Game.instance.area_map).generate()

        Game.instance.floors.append(Game.instance.area_map)
        Game.instance.event_busses.append(Game.instance.event_bus)

    Game.instance.area_map = Game.instance.floors[Game.instance.current_floor-1]
    Game.instance.event_bus = Game.instance.event_busses[Game.instance.current_floor-1]

    Game.instance.area_map.place_on_random_ground(Game.instance.player)
    if config.data.stallion.enabled:
        Game.instance.area_map.place_around(Game.instance.stallion, Game.instance.player.x, Game.instance.player.y)

    Game.instance.game_state = 'playing'
    Game.instance.inventory = []

    # create the list of game messages and their colors, starts empty
    Game.instance.game_messages = []

    # a warm welcoming message!
    message('Another brave knight yearns to bring peace to the land.', colors.red)

    # Gain four levels
    Game.instance.xp_system.get(Game.instance.player).gain_xp(40 + 80 + 160 + 320)


def play_game():
    Game.instance.ui.clear()
    Game.instance.ui.blit_map_and_panel()

    Game.instance.mouse_coord = (0, 0)
    Game.instance.renderer = MapRenderer(Game.instance.player, Game.instance.ui)
    Game.instance.renderer.recompute_fov = True
    Game.instance.renderer.refresh_all()

    Game.instance.current_turn = Game.instance.player
    Game.instance.ui.run()


def init_game():
    Game() # initializes Game.instance

    Game.instance.ui = TdlAdapter(
        "Roguelike",
        screen=(SCREEN_WIDTH, SCREEN_HEIGHT),
        map=(MAP_WIDTH, MAP_HEIGHT),
        panel=(SCREEN_WIDTH, PANEL_HEIGHT),
        fps_limit=LIMIT_FPS
    )

    Game.instance.save_manager = SaveManager(Game)
    Game.instance.keybinder = KeyBinder(Game)
    Game.instance.keybinder.register_all_keybinds_and_events()

    seed = config.get("seed") or int(datetime.now().timestamp())
    Game.instance.random = Random(seed)
    print("Seeding as universe #{}".format(seed))

    Game.instance.event_bus = EventBus()


def main_menu():
    init_game()
    img = image_load('menu_background.png')

    while not Game.instance.ui.event_closed():
        # show the background image, at twice the regular console resolution
        img.blit_2x(Game.instance.ui.root, 0, 0)

        # show the game's title, and some credits!
        title = 'FURUSIYA'
        center = (SCREEN_WIDTH - len(title)) // 2
        Game.instance.ui.draw_root(center, SCREEN_HEIGHT // 2 - 4, title, colors.light_yellow)

        title = 'By nightblade9 and NegativeScript'
        center = (SCREEN_WIDTH - len(title)) // 2
        Game.instance.ui.draw_root(center, SCREEN_HEIGHT - 2, title, colors.light_yellow)

        # show options and wait for the player's choice
        choice = create_menu('', ['Play a new game', 'Continue last game', 'Quit'], 24)

        if choice == 0:  # new game
            new_game()
            play_game()
        if choice == 1:  # load last game
            try:
                Game.instance.save_manager.load()
            except Exception as e:
                message_box('\n No saved game to load.\n', 24)
                continue
            play_game()
        elif choice == 2:  # quit
            break

    print("Terminating ...")

    file_watcher.stop()


if __name__ == '__main__':
    main_menu()

