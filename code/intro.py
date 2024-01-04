import pygame 
from game_settings import *
from support import *
from sprites import Generic
from cutscene import CutSceneOne

class Intro:
    def __init__(self, display_game):
        self.display_surface = pygame.display.get_surface()
        self.display_game = display_game

        #button animation
        self.frames = import_folder('../graphics/button/play')
        self.frame_index = 0

    def animate_button(self,dt):
        self.frame_index += 2 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

        #button
        self.play_button = Button(self.image, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        self.play_button.update(self.display_surface)

    def run(self, dt):
        background = pygame.image.load('../graphics/world/intro.png')
        background_rect = background.get_rect(topleft= (0,0))
        self.display_surface.blit(background, background_rect)
        self.animate_button(dt)
    
    def play_cutscene(self):
        self.display_game.cut_scene_manager.start_cut_scene(CutSceneOne())
        letter_surf = pygame.Surface((20,10))
        letter_surf.fill('white')

        for x, y, __ in self.display_game.tmx_data.get_layer_by_name('Letter').tiles():
            Generic((x * TILE_SIZE,y * TILE_SIZE), letter_surf, [self.display_game.all_sprites, self.display_game.collision_sprites])