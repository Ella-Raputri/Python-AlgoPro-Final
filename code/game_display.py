import pygame 
from game_settings import *
from player import Player
from overlay import Overlay
from sprites import *
from pytmx.util_pygame import load_pygame
from support import import_folder
from transition import Transition
from soil import SoilLayer
from sky import Rain, Sky
from random import randint
from merchant_menu import Menu
from overlay_menu import Overlay_Menu, Inventory
from cutscene import CutSceneManager

class CameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		#the display surface and the offset
		self.display_surface = pygame.display.get_surface()
		self.offset = pygame.math.Vector2()

	def custom_draw(self, player):
		#how much we want to shift the sprite based on the player's movement
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


class Display:
	def __init__(self):
		# get the display surface
		self.display_surface = pygame.display.get_surface()
		#cutscene manager
		self.cut_scene_manager = CutSceneManager(self.display_surface)

		# sprites groups
		#to know which object has to be updated based on player's point of view (camera)
		self.all_sprites = CameraGroup() 
		self.collision_sprites = pygame.sprite.Group() 
		self.tree_sprites = pygame.sprite.Group()
		self.interaction_sprites = pygame.sprite.Group() 
		
		#the soil layer (has to be updated and also contains plant that is collidable)
		self.soil_layer = SoilLayer(self.all_sprites, self.collision_sprites)
		self.setup() #set up game elements

		#the overlay tool and seed status on the bottom left of the screen
		self.overlay = Overlay(self.player)
		#the transition to reset a day
		self.transition = Transition(self.reset, self.player)

		#rain
		self.rain = Rain(self.all_sprites)
		#percentage of the rain
		self.raining = randint(0,10) < 3
		#to update the all soil to water soil tiles if raining
		self.soil_layer.raining = self.raining
		#day-night transition
		self.sky = Sky()

		#shop
		self.menu = Menu(self.player, self.toggle_shop)
		self.shop_active = False #shop is not default open

		#help
		self.help_active = False #help is not defaultly opened
		self.help = Overlay_Menu(self.player, self.toggle_help) 

		#inventory
		self.inventory_active = False #inventory is not default opened
		self.inventory = Inventory(self.player, self.toggle_inventory) 

		#Sound
		#success acquiring plants and woods
		self.success_sound = pygame.mixer.Sound('../audio/success.mp3')
		self.success_sound.set_volume(0.3)

		#background music, (loops=-1) to loop it until player exits
		self.bg_sound = pygame.mixer.Sound('../audio/bg.mp3')
		self.bg_sound.set_volume(0.25)
		self.bg_sound.play(loops=-1)

		#when clicking a button or toggling menus
		self.click_sound = pygame.mixer.Sound('../audio/click.mp3')
		self.click_sound.set_volume(0.3)

	def setup(self):
		#load the map for the game elements
		self.tmx_data = load_pygame('../data/map.tmx')

		#house bottom surface
		for layer in ['HouseFloor', 'HouseFurnitureBottom']:
			#for every tile in the tilelayers, create a Generic object with the layer in house bottom
			for x, y, surf in self.tmx_data.get_layer_by_name(layer).tiles():
				Generic((x * TILE_SIZE,y * TILE_SIZE), surf, self.all_sprites, LAYERS['house bottom'])

		#house top surface
		for layer in ['HouseWalls', 'HouseFurnitureTop']:
			#for every tile in the tilelayers, create a Generic object with the layer main (default)
			for x, y, surf in self.tmx_data.get_layer_by_name(layer).tiles():
				Generic((x * TILE_SIZE,y * TILE_SIZE), surf, self.all_sprites)

		#fence
		for x, y, surf in self.tmx_data.get_layer_by_name('Fence').tiles():
			#for every surface in the tilelayer, create a Generic object with the layer in main
			#it needs collision sprite to restrain the player from moving out of the fences
			Generic((x * TILE_SIZE,y * TILE_SIZE), surf, [self.all_sprites, self.collision_sprites])
			
		#water 
		water_frames = import_folder('../graphics/water') #to animate water
		for x, y, surf in self.tmx_data.get_layer_by_name('Water').tiles():
			#for every surface in the tilelayer, create a Water object with the layer in water (default)
			Water((x * TILE_SIZE,y * TILE_SIZE), water_frames, self.all_sprites)

		#trees 
		for obj in self.tmx_data.get_layer_by_name('Trees'):
			#for every object in the object layer, create a Tree object with the layer in main (default)
			Tree(
				pos = (obj.x, obj.y), 
				surf = obj.image, 
				groups = [self.all_sprites, self.collision_sprites, self.tree_sprites], 
				name = obj.name,
				player_add = self.player_add)

		#wildflowers 
		for obj in self.tmx_data.get_layer_by_name('Decoration'):
			#for every object in the object layer, create a Generic object with the layer in main (default)
			Generic((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites])

		#collision tiles
        #no need to be updated and visible, so don't have to be included in all sprites
		for x, y, surf in self.tmx_data.get_layer_by_name('Collision').tiles():
			#simulate collisions on objects from the other tilelayers
			Generic((x * TILE_SIZE, y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)), self.collision_sprites)

		#the player 
		for obj in self.tmx_data.get_layer_by_name('Player'):
			#player will be first be blitted on the start object in the player object layer
			if obj.name == 'Start':
				self.player = Player(
					pos = (obj.x,obj.y), 
					group = self.all_sprites, 
					collision_sprites = self.collision_sprites,
					all_sprites = self.all_sprites,
					tree_sprites = self.tree_sprites,
					interaction = self.interaction_sprites,
					soil_layer = self.soil_layer,
					toggle_shop = self.toggle_shop,
					toggle_help = self.toggle_help,
					toggle_inventory= self.toggle_inventory,
					tmx_data_map= self.tmx_data,
					cutscene= self.cut_scene_manager)
			
			#if the object is bed, then create an Interaction object, so that we can interact with it (reset the day)
			if obj.name == 'Bed':
				Interaction((obj.x,obj.y), (obj.width,obj.height), self.interaction_sprites, obj.name)

			#if the object is trader, then create an Interaction object, so that we can interact with it (open shop)
			if obj.name == 'Trader':
				Interaction((obj.x,obj.y), (obj.width,obj.height), self.interaction_sprites, obj.name)

			##if the object is feed_cow, then create an Interaction object, so that we can interact with it (feed the cow)
			if obj.name == "Feed_cow":
				Interaction((obj.x,obj.y), (obj.width,obj.height), self.interaction_sprites, obj.name)

			#if the object is table, then create an Interaction object, so that we can interact with it (play specific cutscene)
			if obj.name == "Table":
				Interaction((obj.x,obj.y), (obj.width,obj.height), self.interaction_sprites, obj.name)

		cow_frames = import_folder('../graphics/animal') #to animate cow
		#Cow
		for x, y, surf in self.tmx_data.get_layer_by_name('cow').tiles():
			#for every tile in the tilelayers, create an Animal object with the layer main (default)
			Animal((x * TILE_SIZE,y * TILE_SIZE), cow_frames, [self.all_sprites, self.collision_sprites])
		
		#Cow Farm (Fence)
		for x, y, surf in self.tmx_data.get_layer_by_name('CowFarm').tiles():
			#for every tile in the tilelayers, create a Generic object with the layer main (default)
			Generic((x * TILE_SIZE,y * TILE_SIZE), surf, [self.all_sprites, self.collision_sprites])

		#to set the milk bottle to the first image (the empty one)
		milk_surf_list = import_folder('../graphics/milk/milk_item')
		self.index_milk = 0
		milk_surf = milk_surf_list[self.index_milk]

		for x, y, __ in self.tmx_data.get_layer_by_name('CowMilk').tiles():
			#for every tile in the tilelayers, create a Generic object with the layer main (default)
			Generic((x * TILE_SIZE,y * TILE_SIZE), milk_surf, [self.all_sprites, self.collision_sprites])

		#the floor background, so the layer is ground or the lowest layer
		Generic(
			pos = (0,0),
			surf = pygame.image.load('../graphics/world/ground.png').convert_alpha(), #load the image
			groups = self.all_sprites,
			z = LAYERS['ground'])

	def toggle_shop(self):
		#toggling on and off for the shop
		self.click_sound.play()
		self.shop_active = not self.shop_active
	
	def toggle_help(self):
		#toggling on and off for the help menu
		self.click_sound.play()
		self.help_active = not self.help_active
	
	def toggle_inventory(self):
		#toggling on and off for the inventory
		self.click_sound.play()
		self.inventory_active = not self.inventory_active

	def player_add(self,item):
		#+1 item to the inventory
		self.player.item_inventory[item] += 1
		self.success_sound.play()

	def reset(self):
		#plants growth
		self.soil_layer.update_plants()
		#remove water on the soils
		self.soil_layer.remove_water()

		#randomize the rain again
		self.raining = randint(0,10) < 3
		self.soil_layer.raining = self.raining
		#if it's raining, all plantable soils will become water soils
		if self.raining:
			self.soil_layer.water_all()

		#tree alive again
		for tree in self.tree_sprites.sprites():
			tree.revive()

		#sky color back to day
		self.sky.start_color = [255,255,255]

		#update milk bottle 		
		if self.player.food == True:
			milk_surf_list = import_folder('../graphics/milk/milk_item')

			#if cows are feeded and index_milk is lesser than 4 (because the index milk is from 0 to 4)
			#then index_milk will be added 1
			if self.index_milk < (len(milk_surf_list) - 1):
				self.index_milk += 1

			#if the index_milk = 4, then if we feed the cow again, we will harvest the mik
			#the milk bottle will become empty again
			else:
				self.index_milk = 0

			#create a Generic object based on the updated milk bottle
			milk_surf = milk_surf_list[self.index_milk]
			for x, y, __ in self.tmx_data.get_layer_by_name('CowMilk').tiles():
				Generic((x * TILE_SIZE,y * TILE_SIZE), milk_surf, [self.all_sprites, self.collision_sprites])

		#cow hungry again and grass disappear
		self.player.food = False
		for grass in self.player.grass_sprites:
			grass.kill()

	def plant_collision(self):
		#if there is plant in the soil layer
		if self.soil_layer.plant_sprites:
			#for every plant
			for plant in self.soil_layer.plant_sprites.sprites():
				#if plant is harvestable and the player collides with the plant
				if plant.harvestable and plant.rect.collidepoint(self.player.target_pos):
					#add the crops to the inventory and kill the plant object
					self.player_add(plant.plant_type)
					plant.kill()

					#generate a white mask particle when the plant is killed
					Particle(
						pos = plant.rect.topleft,
						surf = plant.image,
						groups = self.all_sprites,
						z = LAYERS['main']
					)

					#the soil layer can be used to plant seeds again
					self.soil_layer.grid[plant.rect.centery // TILE_SIZE][plant.rect.centerx // TILE_SIZE].remove('P')

	def run(self,dt):
		#run and update all the game elements
		#if no cutscene runs at the moment
		if self.cut_scene_manager.cut_scene_running == False:
			#draw player and its environment based on the camera
			self.all_sprites.custom_draw(self.player)
			#if shop is active and help and inventory is not active, update shop
			if self.shop_active and not self.help_active and not self.inventory_active:
				self.menu.update()
			#if help is active and shop and inventory is not active, update help menu
			elif self.help_active and not self.shop_active and not self.inventory_active:
				self.help.update()
			#if inventory is active and help and shop is not active, update inventory
			elif self.inventory_active and not self.shop_active and not self.help_active:
				self.inventory.update()
			else:
				#update or play cutscenes if player done the missions and press C
				self.player.update_cutscene()
				#update all objects in all sprites
				self.all_sprites.update(dt)
				# player can harvest plant
				self.plant_collision()
				#display the tool and seed overlay
				self.overlay.display()
		else:
			#if cutscene is running, then update and draw scene
			self.cut_scene_manager.update()
			self.cut_scene_manager.draw()
		
		#if it's raining and shop, help, inventory menu is not active, and no cutscene runs
		if self.raining and not self.shop_active and not self.help_active and not self.inventory_active \
			and self.cut_scene_manager.cut_scene_running == False:
			#then update rain drops and rain floors
			self.rain.update()

		#transition if player goes to bed
		if self.player.sleep:
			self.transition.play()
