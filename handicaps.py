import colors
from game import Game
from model import key_binder
from model.helper_functions.message import message

BLIND_SIGHT_RADIUS = 3
HANDICAP_COLOUR = colors.red

def half_health(player):
    fighter = Game.instance.fighter_system.get(player)
    fighter.max_hp = int(fighter.max_hp / 2)
    if fighter.max_hp == 0:
        fighter.max_hp = 1
    fighter.hp = min(fighter.hp, fighter.max_hp)
    message(f"Your max HP halves to {fighter.max_hp}!", HANDICAP_COLOUR)

def half_skill_points(player):
    skill_component = Game.instance.skill_system.get(player)
    skill_component.max_skill_points = int(skill_component.max_skill_points / 2)
    skill_component.skill_points = min(skill_component.skill_points, skill_component.max_skill_points)
    message(f"Your max skill points halve {skill_component.max_skill_points}!", HANDICAP_COLOUR)

def disable_random_skill(player):
    random_skill = key_binder.SKILL_KEYBINDINGS.popitem()
    skill_name = random_skill[0]
    skill_key = random_skill[1].popitem()[0] # tuple of key => lambda, [0] is the key  
    # key is name, value is a dictionary of key => callback
    Game.instance.keybinder.suspend_keybind(skill_key)
    message(f"Your {skill_name} skill ({skill_key} key) is disabled!", HANDICAP_COLOUR)

def blind(player):
    player.sight_radius = BLIND_SIGHT_RADIUS
    message(f"You are struck by blindness!", HANDICAP_COLOUR)

def break_weapon(player):
    # Break if not broken. Otherwise, ya'ne, player feels like BONUS, nothing went
    # bad in this descent :)
    player_fighter = Game.instance.fighter_system.get(player)
    if player_fighter.weapon:
        name = player_fighter.weapon.name
        player_fighter.weapon = None
        message(f"Your {name} breaks!", HANDICAP_COLOUR)
    else:
        message("Your weapon is already broken.", colors.gray)