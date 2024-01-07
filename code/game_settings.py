from pygame.math import Vector2

#game name
GAME_NAME = "Bunn's Christmas Tree Tale"

#screen configuration
SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1280
TILE_SIZE = 64

#overlay positions
OVERLAY_POSITIONS = {
    'tool' : (40, SCREEN_HEIGHT - 15),
    'seed' : (40, SCREEN_HEIGHT - 80)
}

#player tool offset to determine the target position of the used tool 
PLAYER_TOOL_OFFSET = {
	'left': Vector2(-50,40),
	'right': Vector2(50,40),
	'up': Vector2(0,-10),
	'down': Vector2(0,50)
}

#layers of objects
LAYERS = {
	'water': 0,
	'ground': 1,
	'soil': 2,
	'soil water': 3,
	'rain floor': 4,
	'house bottom': 5,
	'main': 6,
	'rain drops': 7
}

#plant's grow speed
GROW_SPEED = {
	'corn': 1,
	'tomato': 0.7
}

#item's sale prices
SALE_PRICES = {
	'corn': 10,
    'milk': 35,
    'tomato': 20,
    'wood': 5
}

#item's purchase prices
PURCHASE_PRICES = {
	'corn': 4,
	'tomato': 5,
    'grass' : 8
}

#keyboard keys input in this game
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
    'H' : 'Open help menu',
    'O' : 'Close menu',
    'Enter': 'Go to bed, open merchant menu, or feed cow',
    'Arrow' : 'Navigate items in merchant menu',
    'C' : 'Start cutscene',
}

#overlay menu's button position
BUTTON_POS = {
    'help' : (1220, 40),
    'inventory' : (1120, 40)
}

#colors that are common in the game
GAME_COLOR = {
    'dialogue box' : (232, 207,166),
    'text': (184,139,98),
    'inventory' : (244,231,196)
}