def half_health(player):
    player.fighter.max_hp = int(player.fighter.max_hp / 2)
    player.fighter.hp = min(player.fighter.hp, player.fighter.max_hp)

def half_skill_points(player):
    pass

def disable_random_skill(player):
    pass