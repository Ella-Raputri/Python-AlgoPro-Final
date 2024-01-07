import pygame, sys
from game_settings import *
from game_display import Display
from intro import Intro

class Game:
	#initialize pygame
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
		pygame.display.set_caption(GAME_NAME)
		self.clock = pygame.time.Clock()
		self.display = Display()
		self.intro = Intro(self.display)
	
	def intro_menu(self):
		while True:
			dt = self.clock.tick() / 1000
			mouse_pos = pygame.mouse.get_pos()
			self.intro.run(dt)

			#checking pygame event
			for event in pygame.event.get():
				#if player clicks quit or press escape, then quit the game
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						pygame.quit()
						sys.exit()

				if event.type == pygame.MOUSEBUTTONDOWN:
					mouse_pos = pygame.mouse.get_pos()
					if self.intro.play_button.checkForInput(mouse_pos):
						self.display.click_sound.play()
						self.intro.play_cutscene()
						self.run_game()

			pygame.display.update()


	def run_game(self):
		#while running the game
		while True:
			#formula for delta time, delta time is used to ensure smooth consistent animation across framerate
			dt = self.clock.tick() / 1000

			#checking pygame event
			for event in pygame.event.get():
				#if player clicks quit or press escape, then quit the game
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						pygame.quit()
						sys.exit()
			
			self.display.run(dt)	
			#run all the game elements and update the display
			pygame.display.update()


#This code will only be executed when we run this program as a script, not an imported module
if __name__ == '__main__':
	game = Game()
	game.intro_menu()
 