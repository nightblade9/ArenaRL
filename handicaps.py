import colors
from model.config import config
from game import Game
from model import key_binder
from model import helper_functions
import random

HANDICAP_COLOUR = colors.red
MINIMUM_SIGHT = 2

# Use if-statements here to dynamically define methods
if config.data.handicaps.allowHealthDecrease:
    def half_health(player):
        decrease_percent = config.data.handicaps.healthDecreasePercent
        fighter = Game.instance.fighter_system.get(player)
        if fighter.max_hp > 1:
            fighter.max_hp = int(fighter.max_hp * (1 - decrease_percent))
            fighter.hp = min(fighter.hp, fighter.max_hp)
            helper_functions.message.message(f"Your max HP drops by {int(decrease_percent * 100)}% to {fighter.max_hp}!", HANDICAP_COLOUR)
        else:
            helper_functions.message.message(f"Your health is already destroyed.")

if config.data.handicaps.allowSpDecrease:
    def half_skill_points(player):
        decrease_percent = config.data.handicaps.skillPointsDecreasePercent
        skill_component = Game.instance.skill_system.get(player)
        if skill_component.max_skill_points > 0:    
            skill_component.max_skill_points = int(skill_component.max_skill_points * (1 - decrease_percent))        
            skill_component.skill_points = min(skill_component.skill_points, skill_component.max_skill_points)
            helper_functions.message.message(f"Your max skill points drop by {int(100 * decrease_percent)}% to {skill_component.max_skill_points}!", HANDICAP_COLOUR)
        else:
            helper_functions.message.message(f"Your skill points are already destroyed.")

if config.data.handicaps.allowDisablingRandomSkill:
    def disable_random_skill(player):
        skill_name = random.choice(list(key_binder.SKILL_KEYBINDINGS.keys()))
        random_skill = key_binder.SKILL_KEYBINDINGS.pop(skill_name)
        # nested dictionaries of name => {key => method}
        key_and_method = random_skill.popitem()
        # key => method
        skill_key = key_and_method[0]

        # key is name, value is a dictionary of key => callback
        Game.instance.keybinder.suspend_keybind(skill_key)
        helper_functions.message.message(f"Your {skill_name} skill ({skill_key} key) is disabled!", HANDICAP_COLOUR)

if config.data.handicaps.allowBlindness:
    def blind(player):
        decrease_radius = config.data.handicaps.blindRadiusDecrease
        if player.sight_radius > MINIMUM_SIGHT:
            player.sight_radius -= decrease_radius
            helper_functions.message.message(f"You are struck by blindness! Your site narrows by {decrease_radius} tiles!", HANDICAP_COLOUR)
        else:
            helper_functions.message.message("You're already too blind.")

if config.data.handicaps.allowWeaponBreakage:
    def break_weapon(player):
        # Break if not broken. Otherwise, ya'ne, player feels like BONUS, nothing went
        # bad in this descent :)
        player_fighter = Game.instance.fighter_system.get(player)
        if player_fighter.weapon:
            name = player_fighter.weapon.name
            player_fighter.weapon = None
            helper_functions.message.message(f"Your {name} breaks!", HANDICAP_COLOUR)
        else:
            helper_functions.message.message("Your weapon is already broken.", colors.gray)