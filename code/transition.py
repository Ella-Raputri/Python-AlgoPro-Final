import pygame
from game_settings import *

class Transition:
	def __init__(self, reset, player):	
		#basic setup
		self.display_surface = pygame.display.get_surface()
		self.reset = reset #reset function
		self.player = player

		#overlay surface
		self.image = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
		#color
		self.color = 255
		#changing color speed
		self.speed = -1

	def play(self):
		#playing color transition from white to black
		self.color += self.speed
		#if the color is black, then change the color slowly to white again
		#by multiplying the speed with -1 while also doing the reset function
		if self.color <= 0:
			self.speed *= -1
			self.color = 0
			self.reset()
		#if the color number is greater than 255, then change the color number back to 255
		#or white and player wakes up, the speed also becomes negative again
		if self.color > 255:
			self.color = 255
			self.player.sleep = False
			self.speed = -1

		#fill the surface with the corresponding color
		self.image.fill((self.color,self.color,self.color))
		self.display_surface.blit(self.image, (0,0), special_flags = pygame.BLEND_RGBA_MULT)