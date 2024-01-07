import pygame
from game_settings import *
from support import *

class Generic(pygame.sprite.Sprite):
	#class for every generic elements in the game
	def __init__(self, pos, surf, groups, z = LAYERS['main']):
		super().__init__(groups)
		#contains image, rect, layer(z), and hitbox
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)
		self.z = z
		self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)

class Interaction(Generic):
	def __init__(self, pos, size, groups, name):
		#has a name, so that we can define what is the interaction
		#when player collides with this object
		surf = pygame.Surface(size)
		super().__init__(pos, surf, groups)
		self.name = name

class Water(Generic):
	def __init__(self, pos, frames, groups):
		#animation setup
		self.frames = frames
		self.frame_index = 0

		#sprite setup
		super().__init__(
				pos = pos, 
				surf = self.frames[self.frame_index], 
				groups = groups, 
				z = LAYERS['water']) 

	def animate(self,dt):
		frame_change = 5
		#animation, change by frame_change and delta time
		self.frame_index += frame_change * dt
		if self.frame_index >= len(self.frames):
			self.frame_index = 0
        #update the image with the new surface
		self.image = self.frames[int(self.frame_index)]

	def update(self,dt):
		#update the water
		self.animate(dt)

class Particle(Generic):
	#particle when plant is destroyed
	def __init__(self, pos, surf, groups, z, duration = 200):
		super().__init__(pos, surf, groups, z)
		#the start time and duration
		self.start_time = pygame.time.get_ticks()
		self.duration = duration

		#generate white surface that is a masked surface from the image 
		mask_surf = pygame.mask.from_surface(self.image)
		new_surf = mask_surf.to_surface()
		new_surf.set_colorkey((0,0,0)) #white color
		self.image = new_surf 

	def update(self,dt):
		current_time = pygame.time.get_ticks()
		#can only be seen for some miliseconds during the duration
		if current_time - self.start_time > self.duration:
			self.kill()

class Tree(Generic):
	def __init__(self, pos, surf, groups, name, player_add):
		#tree attributes
		self.health = 5 
		self.alive = True #by default, alive

		#stump image
		stump_path = f'../graphics/stumps/{"small" if name == "Small" else "large"}.png'
		self.stump_surf = pygame.image.load(stump_path).convert_alpha()

		#tree image
		tree_path = f'../graphics/objects/{"tree_small" if name == "Small" else "tree_medium"}.png'
		self.tree_surf = pygame.image.load(tree_path).convert_alpha()
		super().__init__(pos, surf, groups)

		#add item
		self.player_add = player_add

		#sound
		#when tree is damaged, play axe sound
		self.axe_sound = pygame.mixer.Sound('../audio/axe.wav')
		self.axe_sound.set_volume(0.6)
			
	def damage(self):
		# damaging the tree
		self.health -= 1
		#play sound
		self.axe_sound.play()

	def check_death(self):
		#if health is lesser than 0
		if self.health <= 0:
			#the surface will become stump
			self.image = self.stump_surf
			self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
			self.hitbox = self.rect.copy().inflate(-10,-self.rect.height * 0.6)
			self.alive = False #tree is not alive
			self.player_add('wood') #add wood to player inventory

	def revive(self):
		#tree alive again and has full health
		self.alive = True
		self.health = 5

		#tree image change backs from stump to tree again
		self.image = self.tree_surf
		self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
		self.hitbox = self.rect.copy().inflate(-10,-self.rect.height * 0.6)

	def update(self, dt):
		#update the tree if it's dead
		if self.alive:
			self.check_death()

class Animal(Generic):
	def __init__(self, pos, frames, groups):
		#animation setup
		self.frames = frames
		self.frame_index = 0

		#sprite setup
		super().__init__(
				pos = pos, 
				surf = self.frames[self.frame_index], 
				groups = groups, 
				z = LAYERS['main']) 

	def update(self,dt):
		frame_change = 5
		#animation based on frame change and dt
		self.frame_index += frame_change * dt
		if self.frame_index >= len(self.frames):
			self.frame_index = 0
        #update the image with the new surface
		self.image = self.frames[int(self.frame_index)]