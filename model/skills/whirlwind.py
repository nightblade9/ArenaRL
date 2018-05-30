from game import Game
from elements import Element

class Whirlwind:
    @staticmethod
    def process(player, radius, area_map):
        for obj in area_map.entities:
            if obj.distance(player.x, player.y) <= radius and Game.instance.fighter_system.has(obj) \
            and Game.instance.fighter_system.get(obj).hostile:
                player_fighter = Game.instance.fighter_system.get(player)
                target_fighter = Game.instance.fighter_system.get(obj)
                # attacks and applies elemental damage
                damage = player_fighter.calculate_damage(1, target_fighter)
                target_fighter.take_damage(damage, Element.LIGHTNING)
