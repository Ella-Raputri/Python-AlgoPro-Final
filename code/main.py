import pygame, sys
from game_settings import *
from game_display import Display
from intro import Intro

class Game:
	#initialize game
	def __init__(self):
		#init pygame
		pygame.init()
		#set the screen and the game title
		self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
		pygame.display.set_caption(GAME_NAME)
		#clock will be used to count delta time below
		self.clock = pygame.time.Clock()

		#the game function
		self.display = Display()
		#the intro menu
		self.intro = Intro(self.display)
	
	def intro_menu(self):
	#intro menu state
		while True:
			#counting delta time
			#delta time is used to ensure smooth consistent animation across framerate
			dt = self.clock.tick() / 1000

			#display the intro menu
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

				#if player clicks the play button, then 
				#play click sound, play the first cutscene, and run the game
				if event.type == pygame.MOUSEBUTTONDOWN:
					mouse_pos = pygame.mouse.get_pos()
					if self.intro.play_button.checkForInput(mouse_pos):
						self.display.click_sound.play()
						# self.intro.play_cutscene()
						self.run_game()

			#update display
			pygame.display.update()

	def run_game(self):
		#while running the game
		while True:
			#formula for delta time
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
			
			#run all the game elements and update the display
			self.display.run(dt)
			pygame.display.update()


#This code will only be executed when we run this program as a script, not an imported module
if __name__ == '__main__':
	#make a game object and then run the intro menu
	game = Game()
	game.intro_menu()
 