import pygame, sys
from game_settings import *
from support import *
from sprites import Generic
from cutscene import *

class Player(pygame.sprite.Sprite):
	def __init__(self, pos, group, collision_sprites, all_sprites, tree_sprites, 
			  interaction, soil_layer, toggle_shop, toggle_help, toggle_inventory, tmx_data_map, cutscene):
		super().__init__(group)
		self.import_assets()

		#default image for the player
		self.animation_status = 'down_idle'
		self.frame_index = 0

        #general configuration, getting surface based on the animation status and index
        #after that generate a rect based on the surface
		self.image = self.animations[self.animation_status][self.frame_index]
		self.rect = self.image.get_rect(center = pos)
		self.z = LAYERS['main']

        #movement setup
		self.direction = pygame.math.Vector2()
		self.pos = pygame.math.Vector2(self.rect.center)
		self.speed = 200

		# collision
		self.hitbox = self.rect.copy().inflate((-126,-70))
		self.collision_sprites = collision_sprites

        #timers for using tool
		self.timers = {
			'tool use': Timer(350,self.use_tool),
			'tool switch': Timer(200),
			'seed plant': Timer(350,self.use_seed),
			'seed switch': Timer(200),
		}

		#tools used
		self.tools = ['hoe','axe','water']
		self.tool_index = 0
		self.tool_status = self.tools[self.tool_index]

		#seeds available 
		self.seeds = ['corn', 'tomato']
		self.seed_index = 0
		self.seed_status = self.seeds[self.seed_index]

		#player's inventory by default
		self.item_inventory = {
			'corn':   0,
			'milk': 0,
			'tomato': 0,
			'wood':   0
		}
		self.seed_inventory = {
			'corn': 5,
			'tomato' : 5
		}
		self.other_inventory = {
			'grass': 5
		}
		self.money = 0

		#interaction
		self.all_sprites = all_sprites
		self.tree_sprites = tree_sprites
		self.milk_sprites = pygame.sprite.Group()
		self.interaction = interaction
		self.sleep = False
		self.soil_layer = soil_layer
		self.toggle_shop = toggle_shop
		self.toggle_help = toggle_help
		self.toggle_inventory = toggle_inventory

		#sound
		self.water_sound = pygame.mixer.Sound('../audio/water.mp3')
		self.water_sound.set_volume(0.3)
		self.grass_sound = pygame.mixer.Sound('../audio/grass.mp3')
		self.grass_sound.set_volume(0.4)
		self.milk_sound = pygame.mixer.Sound('../audio/milk.mp3')
		self.milk_sound.set_volume(0.5)

		#button
		self.display_surface = pygame.display.get_surface()
		self.font = pygame.font.Font('../font/LycheeSoda.ttf', 40)
		self.help_image = pygame.image.load('../graphics/button/help.png')
		self.help_image = pygame.transform.rotozoom(self.help_image, 0, 3)
		self.inventory_image = pygame.image.load('../graphics/button/inventory.png')
		self.inventory_image = pygame.transform.rotozoom(self.inventory_image, 0, 4)

		#animal
		self.food = False
		self.cow_max_age = 5
		self.cow_age = 0
		self.harvest_milk = False
		self.tmx_data = tmx_data_map

		#cutscene
		self.cut_scene_manager = cutscene


	def import_assets(self):
        #importing assets for player animation
        #initialize a dictionary
		self.animations = {'up': [],'down': [],'left': [],'right': [],
						   'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
						   'right_hoe':[],'left_hoe':[],'up_hoe':[],'down_hoe':[],
						   'right_axe':[],'left_axe':[],'up_axe':[],'down_axe':[],
						   'right_water':[],'left_water':[],'up_water':[],'down_water':[]}

        #getting the full path for the folder and then append the image surface to corresponding keys
		for animation in self.animations.keys():
			full_path = '../graphics/character/' + animation
			self.animations[animation] = import_folder(full_path)

	def animate(self,dt):
		frame_change = 4
		#if frame_index greater than number of surfaces in the animation frame, then 
		#make it back to the beginning state
		self.frame_index += frame_change * dt
		if self.frame_index >= len(self.animations[self.animation_status]):
			self.frame_index = 0
		#update the image with the new surface
		self.image = self.animations[self.animation_status][int(self.frame_index)]

	def input(self):
        #get input to determine which direction player moves
		keys = pygame.key.get_pressed()

        #we can only move and start using a tool when we are not using tools
		if not self.timers['tool use'].active and not self.sleep:
            #get and set movement's animation and direction of the player
			if keys[pygame.K_w]:
				self.direction.y = -1
				self.animation_status = 'up'
			elif keys[pygame.K_s]:
				self.direction.y = 1
				self.animation_status = 'down'
			else:
				self.direction.y = 0

			if keys[pygame.K_d]:
				self.direction.x = 1
				self.animation_status = 'right'
			elif keys[pygame.K_a]:
				self.direction.x = -1
				self.animation_status = 'left'
			else:
				self.direction.x = 0

            #activate the timer when player start using a tool and set the direction to (0,0)
            #to prevent player moving when using a tool
			if keys[pygame.K_SPACE]:
				self.timers['tool use'].activate()
				self.direction = pygame.math.Vector2()
				self.frame_index = 0

            #player can only switch tool when player are not in the middle of switching tool
			if keys[pygame.K_q] and not self.timers['tool switch'].active:
				self.timers['tool switch'].activate()
				self.tool_index += 1
				self.tool_index = self.tool_index if self.tool_index < len(self.tools) else 0
				self.tool_status = self.tools[self.tool_index]

            #activate the timer when player start planting a seed and set the direction to (0,0)
            #to prevent player moving when planting
			if keys[pygame.K_j]:
				self.timers['seed plant'].activate()
				self.direction = pygame.math.Vector2()
				self.frame_index = 0

            #player can only switch tool when player are not in the middle of switching tool
			if keys[pygame.K_i] and not self.timers['seed switch'].active:
				self.timers['seed switch'].activate()
				self.seed_index += 1
				self.seed_index = self.seed_index if self.seed_index < len(self.seeds) else 0
				self.seed_status = self.seeds[self.seed_index]

			#trigger help menu
			if keys[pygame.K_h]:
				self.toggle_help()
			
			#trigger inventory menu
			if keys[pygame.K_p]:
				self.toggle_inventory()

			#trigger transition if player go to bed
			if keys[pygame.K_RETURN]:
				collided_interaction_sprite = pygame.sprite.spritecollide(self,self.interaction,False)
				if collided_interaction_sprite:
					if collided_interaction_sprite[0].name == 'Trader':
						self.toggle_shop()

					elif collided_interaction_sprite[0].name == 'Feed_cow':
						if self.harvest_milk == False:
							self.give_food()
							self.grass_sound.play()	
						else:
							self.milk_sound.play()
							self.get_milk()	
					else:
						self.animation_status = 'down_idle'
						self.sleep = True

			#checking mouse event
			mouse_pos = pygame.mouse.get_pos()
			self.button_setup()

			for event in pygame.event.get():
				#trigger help menu
				if event.type == pygame.MOUSEBUTTONDOWN:
					if self.help_button.checkForInput(mouse_pos):
						self.toggle_help()
					elif self.inventory_button.checkForInput(mouse_pos):
						self.toggle_inventory()

				#exit the game
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						pygame.quit()
						sys.exit()

	def button_setup(self):
		#help button
		self.help_button = Button(image=self.help_image, 
					   pos=BUTTON_POS['help'])

		self.help_button.update(self.display_surface)

		#help button
		self.inventory_button = Button(image=self.inventory_image, 
					   pos=BUTTON_POS['inventory'])

		self.inventory_button.update(self.display_surface)

	def get_status(self):	
        #to change the animation when player goes idle
		if self.direction.magnitude() == 0:
			self.animation_status = self.animation_status.split('_')[0] + '_idle'

        #to change animation when player use particular tool
		if self.timers['tool use'].active:
			self.animation_status = self.animation_status.split('_')[0] + '_' + self.tool_status

	def update_timers(self):
		for timer in self.timers.values():
			timer.update()

	def collision(self, direction):
		 #if the sprite has the attribute of hitbox and it coliides with the player's hitbox
		for sprite in self.collision_sprites.sprites():
			if hasattr(sprite, 'hitbox'):
				if sprite.hitbox.colliderect(self.hitbox):
					if direction == 'horizontal':
						if self.direction.x > 0: #the player moving right
							self.hitbox.right = sprite.hitbox.left
						if self.direction.x < 0: #the player moving left
							self.hitbox.left = sprite.hitbox.right
                        #update the rect based on the hitbox
						self.rect.centerx = self.hitbox.centerx
						self.pos.x = self.hitbox.centerx

					if direction == 'vertical':
						if self.direction.y > 0: #the player moving down
							self.hitbox.bottom = sprite.hitbox.top
						if self.direction.y < 0: #the player moving up
							self.hitbox.top = sprite.hitbox.bottom
                        #update the rect based on the hitbox
						self.rect.centery = self.hitbox.centery
						self.pos.y = self.hitbox.centery

	def move(self,dt):
		#normalize the speed of objects when moving diagonal
		if self.direction.magnitude() > 0:
			self.direction = self.direction.normalize()

		#horizontal movement
		self.pos.x += self.direction.x * self.speed * dt
		self.hitbox.centerx = round(self.pos.x)
		self.rect.centerx = self.hitbox.centerx
		self.collision('horizontal')

		#vertical movement
		self.pos.y += self.direction.y * self.speed * dt
		self.hitbox.centery = round(self.pos.y)
		self.rect.centery = self.hitbox.centery
		self.collision('vertical')

	def use_tool(self):
		if self.tool_status == 'hoe':
			self.soil_layer.get_hit(self.target_pos)
		
		if self.tool_status == 'axe':
			for tree in self.tree_sprites.sprites():
				if tree.rect.collidepoint(self.target_pos):
					tree.damage()
		
		if self.tool_status == 'water':
			self.water_sound.play()
			self.soil_layer.water(self.target_pos)

	def get_target_pos(self):
		self.target_pos = self.rect.center + PLAYER_TOOL_OFFSET[self.animation_status.split('_')[0]]

	def use_seed(self):
		if self.seed_inventory[self.seed_status] > 0 and self.soil_layer.check_plantable(self.target_pos):
			self.soil_layer.plant_seed(self.target_pos, self.seed_status)
			self.seed_inventory[self.seed_status] -= 1

	def give_food(self):
		if self.other_inventory['grass'] > 0 and self.food == False:
			self.other_inventory['grass'] -= 1
			self.food = True
			self.cow_age += 1
			grass_surf = pygame.image.load('../graphics/milk/grass.png').convert_alpha()
			for x, y, __ in self.tmx_data.get_layer_by_name('CowFood').tiles():
				Generic((x * TILE_SIZE,y * TILE_SIZE), grass_surf, [self.all_sprites, self.collision_sprites, self.milk_sprites])

		if self.cow_age >= self.cow_max_age: 
			self.harvest_milk = True
	
	def get_milk(self):
		if self.harvest_milk:
			self.item_inventory['milk'] += 1
			self.harvest_milk = False
			self.cow_age = 0

			#milk bottle become empty again
			milk_surf = pygame.image.load('../graphics/milk/milk_item/0.png').convert_alpha()
			for x, y, __ in self.tmx_data.get_layer_by_name('CowMilk').tiles():
				Generic((x * TILE_SIZE,y * TILE_SIZE), milk_surf, [self.all_sprites, self.collision_sprites])

	def update(self, dt):
		#update the player's position, animation, timer, etc based on the input
		self.input()
		self.get_status()
		self.update_timers()
		self.get_target_pos()

		self.move(dt)
		self.animate(dt)

	def update_cutscene(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_c]:
			if 'cutscene3' in self.cut_scene_manager.cut_scenes_complete:
				collided_interaction_sprite = pygame.sprite.spritecollide(self,self.interaction,False)
				if collided_interaction_sprite:
					if collided_interaction_sprite[0].name == 'Table':
						self.cut_scene_manager.start_cut_scene(CutSceneFour())
						christmas_tree_surf = pygame.image.load('../graphics/dialogue/cutscene4/christmas_tree.png').convert_alpha()
						for x, y, __ in self.tmx_data.get_layer_by_name('ChristmasTree').tiles():
							Generic((x * TILE_SIZE,y * TILE_SIZE), christmas_tree_surf, [self.all_sprites, self.collision_sprites])

			elif 'cutscene2' in self.cut_scene_manager.cut_scenes_complete:
				if self.money >= 200:
					self.cut_scene_manager.start_cut_scene(CutSceneThree())
					self.money += 1800

			elif 'cutscene1' in self.cut_scene_manager.cut_scenes_complete:
				collided_interaction_sprite = pygame.sprite.spritecollide(self,self.interaction,False)
				if collided_interaction_sprite:
					if collided_interaction_sprite[0].name == 'Table':
						self.cut_scene_manager.start_cut_scene(CutSceneTwo())
