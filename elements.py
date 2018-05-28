from enum import Enum
from game import Game

class Element(Enum):
    # Fire beats ice beats earth beats lightning beats fire
    FIRE = 1
    ICE = 2
    EARTH = 3
    LIGHTNING = 4
    
def apply_elemental_damage(attacker, target, base_damage):
    """Uber hack to apply element damage"""
    fighter = Game.instance.fighter_system.get(attacker.owner)
    my_weapon = fighter.weapon if fighter is not None else None
    target_elemental = getattr(target, "elemental", None)
    if my_weapon is not None and my_weapon.elemental is not None and target_elemental is not None:
        damage_multipler = _get_multiplier(my_weapon.elemental, target_elemental)
        return base_damage * damage_multipler
    else:
        return base_damage

# eg. fire beats ice, fire vs. ice => 2x
# but ice vs. fire => 0.5x
def _get_multiplier(attacker_elemental, defender_elemental):
    if attacker_elemental == Element.FIRE and defender_elemental == Element.ICE:
        return 2
    elif attacker_elemental == Element.ICE and defender_elemental == Element.EARTH:
        return 2
    elif attacker_elemental == Element.EARTH and defender_elemental == Element.LIGHTNING:
        return 2
    elif attacker_elemental == Element.LIGHTNING and defender_elemental == Element.FIRE:
        return 2
    else:
        if attacker_elemental == Element.ICE and defender_elemental == Element.FIRE:
            return 0.5
        elif attacker_elemental == Element.EARTH and defender_elemental == Element.ICE:
            return 0.5
        elif attacker_elemental == Element.LIGHTNING and defender_elemental == Element.EARTH:
            return 0.5
        elif attacker_elemental == Element.FIRE and defender_elemental == Element.LIGHTNING:
            return 0.5
    return 1 # non-interacting, return 1x damage