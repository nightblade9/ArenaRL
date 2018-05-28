from game import Game

class EarthStab:
    @staticmethod
    def process(player, radius, area_map):
        for obj in area_map.entities:
            if (obj.distance(player.x, player.y) <= radius and
                    Game.instance.fighter_system.has(obj) and
                    Game.instance.fighter_system.get(obj).hostile and
                    (obj.x == player.x or obj.y == player.y) # veritcally/horizontally lined up with player
            ):
                Game.instance.fighter_system.get(player).attack(obj)
