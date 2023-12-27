import pygame 
from game_settings import *
from player import Player
from overlay import Overlay
from sprites import Generic, Water, WildFlower, Tree, Interaction, Particle
from pytmx.util_pygame import load_pygame
from support import *
from transition import Transition
from soil import SoilLayer
from sky import Rain, Sky
from random import randint
from merchant_menu import Menu
from overlay_menu import Overlay_Menu, Inventory

class Display:
	def __init__(self):
		# get the display surface
		self.display_surface = pygame.display.get_surface()

		# sprites groups
		self.all_sprites = CameraGroup()
		self.collision_sprites = pygame.sprite.Group()
		self.tree_sprites = pygame.sprite.Group()
		self.interaction_sprites = pygame.sprite.Group()
		
		self.soil_layer = SoilLayer(self.all_sprites, self.collision_sprites)
		self.setup()
		self.overlay = Overlay(self.player)
		self.transition = Transition(self.reset, self.player)

		#sky
		self.rain = Rain(self.all_sprites)
		self.raining = randint(0,10) < 3
		self.soil_layer.raining = self.raining
		self.sky = Sky()

		#shop
		self.menu = Menu(self.player, self.toggle_shop)
		self.shop_active = False

		#help
		self.help_active = False
		self.help = Overlay_Menu(self.player, self.toggle_help)

		#inventory
		self.inventory_active = False
		self.inventory = Inventory(self.player, self.toggle_inventory)

		#sound
		self.success_sound = pygame.mixer.Sound('../audio/success.wav')
		self.success_sound.set_volume(0.5)
		self.bg_sound = pygame.mixer.Sound('../audio/bg.mp3')
		self.bg_sound.set_volume(0.4)
		self.bg_sound.play(loops=-1)

	def setup(self):
		#set up the game element
		tmx_data = load_pygame('../data/map.tmx')

		#house bottom surface
		for layer in ['HouseFloor', 'HouseFurnitureBottom']:
			for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
				Generic((x * TILE_SIZE,y * TILE_SIZE), surf, self.all_sprites, LAYERS['house bottom'])

		#house top surface
		for layer in ['HouseWalls', 'HouseFurnitureTop']:
			for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
				Generic((x * TILE_SIZE,y * TILE_SIZE), surf, self.all_sprites)

		#fence
		for x, y, surf in tmx_data.get_layer_by_name('Fence').tiles():
			Generic((x * TILE_SIZE,y * TILE_SIZE), surf, [self.all_sprites, self.collision_sprites])
		
		#fence for cow farm
		for x, y, surf in tmx_data.get_layer_by_name('CowFarm').tiles():
			Generic((x * TILE_SIZE,y * TILE_SIZE), surf, [self.all_sprites, self.collision_sprites])

		#water 
		water_frames = import_folder('../graphics/water')
		for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
			Water((x * TILE_SIZE,y * TILE_SIZE), water_frames, self.all_sprites)

		#trees 
		for obj in tmx_data.get_layer_by_name('Trees'):
			Tree(
				pos = (obj.x, obj.y), 
				surf = obj.image, 
				groups = [self.all_sprites, self.collision_sprites, self.tree_sprites], 
				name = obj.name,
				player_add = self.player_add)

		#wildflowers 
		for obj in tmx_data.get_layer_by_name('Decoration'):
			WildFlower((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites])

		#collision tiles
        #no need to be updated, so dont have to be include in all sprites
		for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():
			Generic((x * TILE_SIZE, y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)), self.collision_sprites)

		#the player 
		for obj in tmx_data.get_layer_by_name('Player'):
			if obj.name == 'Start':
				self.player = Player(
					pos = (obj.x,obj.y), 
					group = self.all_sprites, 
					collision_sprites = self.collision_sprites,
					tree_sprites = self.tree_sprites,
					interaction = self.interaction_sprites,
					soil_layer = self.soil_layer,
					toggle_shop = self.toggle_shop,
					toggle_help = self.toggle_help,
					toggle_inventory= self.toggle_inventory)
			
			if obj.name == 'Bed':
				Interaction((obj.x,obj.y), (obj.width,obj.height), self.interaction_sprites, obj.name)

			if obj.name == 'Trader':
				Interaction((obj.x,obj.y), (obj.width,obj.height), self.interaction_sprites, obj.name)
			
			if obj.name == "Fishing":
				Interaction((obj.x,obj.y), (obj.width,obj.height), self.interaction_sprites, obj.name)

		#the floor background
		Generic(
			pos = (0,0),
			surf = pygame.image.load('../graphics/world/ground.png').convert_alpha(),
			groups = self.all_sprites,
			z = LAYERS['ground'])

	def toggle_shop(self):
		#toggling on and off for the shop
		self.shop_active = not self.shop_active
	
	def toggle_help(self):
		self.help_active = not self.help_active
	
	def toggle_inventory(self):
		self.inventory_active = not self.inventory_active

	def player_add(self,item):
		#item inventory
		self.player.item_inventory[item] += 1
		self.success_sound.play()

	def reset(self):
		#plants
		self.soil_layer.update_plants()
		#soils
		self.soil_layer.remove_water()

		#randomize the rain
		self.soil_layer.raining = self.raining
		self.raining = randint(0,10) < 3
		if self.raining:
			self.soil_layer.water_all()

		#tree alive again
		for tree in self.tree_sprites.sprites():
			tree.revive()

		#sky color back to the day
		self.sky.start_color = [255,255,255]

	def plant_collision(self):
		if self.soil_layer.plant_sprites:
			for plant in self.soil_layer.plant_sprites.sprites():
				if plant.harvestable and plant.rect.collidepoint(self.player.target_pos):
					self.player_add(plant.plant_type)
					plant.kill()
					Particle(
						pos = plant.rect.topleft,
						surf = plant.image,
						groups = self.all_sprites,
						z = LAYERS['main']
					)
					self.soil_layer.grid[plant.rect.centery // TILE_SIZE][plant.rect.centerx // TILE_SIZE].remove('P')

	def run(self,dt):
		#run all the game elements
		self.all_sprites.custom_draw(self.player)

		#update
		if self.shop_active and not self.help_active and not self.inventory_active:
			self.menu.update()
		elif self.help_active and not self.shop_active and not self.inventory_active:
			self.help.update()
		elif self.inventory_active and not self.shop_active and not self.help_active:
			self.inventory.update()
		else:
			self.all_sprites.update(dt)
			self.plant_collision()

		self.overlay.display()
		
		#if raining
		if self.raining and not self.shop_active:
			self.rain.update()

		#daytime transition
		self.sky.display(dt)

		#transition if player goes to bed
		if self.player.sleep:
			self.transition.play()


class CameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.offset = pygame.math.Vector2()

	def custom_draw(self, player):
		#how much we want to shift the sprite based on the player
		self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
		self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

		#it is sorted to draw the layers based on the y index
        #if the player y is lesser than the object, then the player will be blitted behind that object
		for layer in LAYERS.values():
			for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
				if sprite.z == layer:
					offset_rect = sprite.rect.copy()
					offset_rect.center -= self.offset
					self.display_surface.blit(sprite.image, offset_rect)