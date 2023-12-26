import pygame, sys
from game_settings import *
from game_display import Display

class Game:
	#initialize pygame
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
		pygame.display.set_caption('Sprout Valley')
		self.clock = pygame.time.Clock()
		self.display = Display()

	def run(self):
		#while running the game
		while True:
			#checking pygame event
			for event in pygame.event.get():
				#if player clicks quit or press escape, then quit the game
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						pygame.quit()
						sys.exit()

			#formula for delta time, delta time is used to ensure smooth consistent animation across framerate
			dt = self.clock.tick() / 1000
			#run all the game elements and update the display
			self.display.run(dt)
			pygame.display.update()


#This code will only be executed when we run this program as a script, not an imported module
if __name__ == '__main__':
	game = Game()
	game.run()
