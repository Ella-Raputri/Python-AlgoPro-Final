import pygame
from game_settings import *
from random import randint, choice
from support import *

class Generic(pygame.sprite.Sprite):
	#class for every generic elements in the game
	def __init__(self, pos, surf, groups, z = LAYERS['main']):
		super().__init__(groups)
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)
		self.z = z
		self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)

class Interaction(Generic):
	def __init__(self, pos, size, groups, name):
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
		self.frame_index += 5 * dt
		if self.frame_index >= len(self.frames):
			self.frame_index = 0
        #update the image with the new surface
		self.image = self.frames[int(self.frame_index)]

	def update(self,dt):
		self.animate(dt)

class WildFlower(Generic):
	def __init__(self, pos, surf, groups):
		super().__init__(pos, surf, groups)
		self.hitbox = self.rect.copy().inflate(-20,-self.rect.height * 0.9)

class Particle(Generic):
	#particle when tree or apple is destroyed
	def __init__(self, pos, surf, groups, z, duration = 200):
		super().__init__(pos, surf, groups, z)
		self.start_time = pygame.time.get_ticks()
		self.duration = duration

		#white surface 
		mask_surf = pygame.mask.from_surface(self.image)
		new_surf = mask_surf.to_surface()
		new_surf.set_colorkey((0,0,0))
		self.image = new_surf

	def update(self,dt):
		current_time = pygame.time.get_ticks()
		if current_time - self.start_time > self.duration:
			self.kill()

class Tree(Generic):
	def __init__(self, pos, surf, groups, name, player_add):
		#tree attributes
		self.health = 5
		self.alive = True
		stump_path = f'../graphics/stumps/{"small" if name == "Small" else "large"}.png'
		self.stump_surf = pygame.image.load(stump_path).convert_alpha()
		tree_path = f'../graphics/objects/{"tree_small" if name == "Small" else "tree_medium"}.png'
		self.tree_surf = pygame.image.load(tree_path).convert_alpha()
		super().__init__(pos, surf, groups)

		#add item
		self.player_add = player_add

		#sound
		self.axe_sound = pygame.mixer.Sound('../audio/axe.mp3')
		
	
	def damage(self):
		# damaging the tree
		self.health -= 1
		#play sound
		self.axe_sound.play()

	def check_death(self):
		if self.health <= 0:
			self.image = self.stump_surf
			self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
			self.hitbox = self.rect.copy().inflate(-10,-self.rect.height * 0.6)
			self.alive = False
			self.player_add('wood')

	def revive(self):
		self.alive = True
		self.health = 5
		self.image = self.tree_surf
		self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
		self.hitbox = self.rect.copy().inflate(-10,-self.rect.height * 0.6)

	def update(self, dt):
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

	def animate(self,dt):
		self.frame_index += 5 * dt
		if self.frame_index >= len(self.frames):
			self.frame_index = 0
        #update the image with the new surface
		self.image = self.frames[int(self.frame_index)]

	def update(self,dt):
		self.animate(dt)