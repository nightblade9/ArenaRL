SCREEN_WIDTH = 60
SCREEN_HEIGHT = 40

# size of the map
MAP_WIDTH = 60
MAP_HEIGHT = 33

# sizes and coordinates relevant for the GUI
BAR_WIDTH = 20
PANEL_HEIGHT = 5
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT
MSG_X = BAR_WIDTH + 2
MSG_WIDTH = SCREEN_WIDTH - BAR_WIDTH - 2
MSG_HEIGHT = PANEL_HEIGHT - 1
INVENTORY_WIDTH = 50

# spell values
HEAL_AMOUNT = 4
LIGHTNING_DAMAGE = 20
LIGHTNING_RANGE = 5
CONFUSE_RANGE = 8
CONFUSE_NUM_TURNS = 10
FIREBALL_RADIUS = 3
FIREBALL_DAMAGE = 12

FOV_ALGO = 'BASIC'
FOV_LIGHT_WALLS = True

LIMIT_FPS = 20  # 20 frames-per-second maximum

DELTA_UP = (0, -1)
DELTA_DOWN = (0, 1)
DELTA_LEFT = (-1, 0)
DELTA_RIGHT = (1, 0)
