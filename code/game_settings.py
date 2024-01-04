from pygame.math import Vector2

#game name
GAME_NAME = 'A Farm\'s Christmas Tree Tale'

#screen configuration
SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1280
TILE_SIZE = 64

#overlay
OVERLAY_POSITIONS = {
    'tool' : (40, SCREEN_HEIGHT - 15),
    'seed' : (40, SCREEN_HEIGHT - 80)
}

PLAYER_TOOL_OFFSET = {
	'left': Vector2(-50,40),
	'right': Vector2(50,40),
	'up': Vector2(0,-10),
	'down': Vector2(0,50)
}

LAYERS = {
	'water': 0,
	'ground': 1,
	'soil': 2,
	'soil water': 3,
	'rain floor': 4,
	'house bottom': 5,
	'ground plant': 6,
	'main': 7,
	'house top': 8,
	'fruit': 9,
	'rain drops': 10
}

GROW_SPEED = {
	'corn': 1,
	'tomato': 0.7
}

SALE_PRICES = {
	'corn': 10,
    'milk': 35,
    'tomato': 20,
    'wood': 5
}

PURCHASE_PRICES = {
	'corn': 4,
	'tomato': 5,
    'grass' : 8
}

KEYBOARD_KEYS = {
    'Esc' : 'Quit the game',
    'A' : 'Move left',
    'D' : 'Move right',
    'W' : 'Move up',
    'S' : 'Move down',
    'Space' : 'Use tool and buy/sell things',
    'Q' : 'Switch tool',
    'J' : 'Plant seed',
    'I' : 'Switch seed',
    'P' : 'Check inventory',
    'O' : 'Close menu',
    'Enter': 'Go to bed or open merchant menu',
    'Arrow' : 'Navigate items in merchant menu',
    'C' : 'Start cutscene',
}

BUTTON_POS = {
    'help' : (1220, 40),
    'inventory' : (1120, 40)
}