from os import walk
import pygame

def import_folder(path):
	#import folder and its content
	surface_list = []

	#get the image files names, generate a path for them, and then make them a surface
	for _, __, img_files in walk(path):
		for image in img_files:
			full_path = path + '/' + image
			image_surf = pygame.image.load(full_path).convert_alpha()
			surface_list.append(image_surf)
	return surface_list


def import_folder_dict(path):
	surface_dict = {}

	#get the image files names, generate a path for them, and then make them a surface
	for _, __, img_files in walk(path):
		for image in img_files:
			full_path = path + '/' + image
			image_surf = pygame.image.load(full_path).convert_alpha()
			surface_dict[image.split('.')[0]] = image_surf
	return surface_dict


class Timer:
#timer to know the duration of a player when doing something
	def __init__(self,duration,func = None):
		self.duration = duration
		self.func = func
		self.start_time = 0
		self.active = False

	def activate(self):
		#when the timer is activated
		self.active = True
		self.start_time = pygame.time.get_ticks()

	def deactivate(self):
		#when the timer is deactivated
		self.active = False
		self.start_time = 0

	def update(self):
		#update timer
		current_time = pygame.time.get_ticks()
		if current_time - self.start_time >= self.duration:
			if self.func and self.start_time != 0:
				self.func()
			self.deactivate()


class Button:
	def __init__(self, image, pos):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False