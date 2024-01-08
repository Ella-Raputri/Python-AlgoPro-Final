import pygame 
from game_settings import *
from support import *
from sprites import Generic
from cutscene import CutSceneOne

class Intro:
    def __init__(self, display_game):
        self.display_surface = pygame.display.get_surface() #display screen
        self.display_game = display_game #game function
        self.topic_font = pygame.font.Font('../font/LycheeSoda.ttf', 100) #topic font
        self.text_font = pygame.font.Font('../font/LycheeSoda.ttf', 30) #Bunn's dialogue font

        #button animation
        self.frames = import_folder('../graphics/button/play')
        self.frame_index = 0

        #character animation
        self.chara_frames = import_folder('../graphics/world/intro_emote')
        self.chara_frame_index = 0
    
    def blit_all(self):
        #load the Christmas hat image, rotate and scale it, then blit it
        hat_surf = pygame.image.load('../graphics/world/hat.png').convert_alpha()
        hat_surf = pygame.transform.rotozoom(hat_surf, 50, 1.5)
        hat_rect = hat_surf.get_rect(topleft=(110, 0))
        self.display_surface.blit(hat_surf, hat_rect)

        #load the Christmas tree image and blit it
        tree_surf = pygame.image.load('../graphics/world/christmas_tree.png').convert_alpha()
        tree_rect = tree_surf.get_rect(topleft=(1050, 0))
        self.display_surface.blit(tree_surf, tree_rect)

        #load the first part of the topic text as a surface and blit it
        topic_surf1 = self.topic_font.render((GAME_NAME.split()[0] + " " + GAME_NAME.split()[1]).upper(), False, 'chartreuse4')
        topic_rect1 = topic_surf1.get_rect(center= (SCREEN_WIDTH/2, 100))
        self.display_surface.blit(topic_surf1, topic_rect1)

        #load the second part of the topic text as a surface and blit it
        topic_surf2 = self.topic_font.render((GAME_NAME.split()[2] + " " + GAME_NAME.split()[3]).upper(), False, 'darkgreen')
        topic_rect2 = topic_surf2.get_rect(center= (SCREEN_WIDTH/2, 200))
        self.display_surface.blit(topic_surf2, topic_rect2)

        #load the dialogue box and blit it
        dialog_surf = pygame.image.load('../graphics/world/dialog.png').convert_alpha()
        dialog_rect = dialog_surf.get_rect(topleft=(350, 500))
        self.display_surface.blit(dialog_surf, dialog_rect)

        #load the dialogue text and blit it
        text_surf = self.text_font.render("Hello, I'm Bunn and this is my Christmas story.", False, 'Black')
        text_rect = text_surf.get_rect(topleft=(400, 560))
        self.display_surface.blit(text_surf, text_rect)

    def animate_all(self,dt):
        #button animation
        self.frame_index += 2 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

        #the play button
        self.play_button = Button(self.image, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        self.play_button.update(self.display_surface)

        #chara animation
        self.chara_frame_index += 2 * dt
        if self.chara_frame_index >= len(self.chara_frames):
            self.chara_frame_index = 0

        #load the chara image based on the index and blit it
        self.chara_image = self.chara_frames[int(self.chara_frame_index)]
        self.chara_rect = self.chara_image.get_rect(topleft=(70, 425))
        self.display_surface.blit(self.chara_image, self.chara_rect)

    def run(self, dt):
        #display the background image on the screen
        background = pygame.image.load('../graphics/world/intro.png').convert()
        background_rect = background.get_rect(topleft= (0,0))
        self.display_surface.blit(background, background_rect)

        self.blit_all() #blit objects
        self.animate_all(dt) #animate objects
    
    def play_cutscene(self):
        #start cutscene one 
        self.display_game.cut_scene_manager.start_cut_scene(CutSceneOne())

        #create a letter Generic object besides the table after cutscene1 
        letter_surf = pygame.Surface((20,10))
        letter_surf.fill('white')

        for x, y, __ in self.display_game.tmx_data.get_layer_by_name('Letter').tiles():
            Generic((x * TILE_SIZE,y * TILE_SIZE), letter_surf, 
                    [self.display_game.all_sprites, self.display_game.collision_sprites])