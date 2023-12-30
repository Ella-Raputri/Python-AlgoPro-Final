import pygame
from game_settings import *

def draw_text(screen, text, size, color, x, y):
    font = pygame.font.Font('../font/LycheeSoda.ttf', size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

def blit_bg_image(screen, path):
    bg_pict = pygame.image.load(f'../graphics/dialogue/{path}')
    bg_rect = bg_pict.get_rect(topleft=(0,0))
    screen.blit(bg_pict, bg_rect)

def draw_chara(screen, path):
    chara_surf = pygame.image.load((f'../graphics/dialogue/{path}'))
    chara_rect = chara_surf.get_rect(topleft=(65,510))
    screen.blit(chara_surf, chara_rect)

def draw_dialog_box(screen):
    dialog_pict = pygame.image.load(f'../graphics/dialogue/dialog_box.png')
    dialog_rect = dialog_pict.get_rect(topleft=(0,450))
    screen.blit(dialog_pict, dialog_rect)

class CutSceneOne:
    def __init__(self):
        # Variables
        self.name = 'cutscene1'
        self.step = 0
        self.cut_scene_running = True

        # Dialogue
        self.setup()
        self.text_counter = 0

    def setup(self):
        self.text={}
        file_story1 = open("story1.txt", "r")
        for index, item in enumerate(file_story1.readlines()):
            self.text[index] = item

    def update(self):
        pressed = pygame.key.get_pressed()
        space = pressed[pygame.K_LCTRL]
        
        for i in range(0, len(self.text)):
            if self.step < len(self.text) - 1:
                if int(self.text_counter) < len(self.text[i]):
                    self.text_counter += 0.05
                else:
                    if space:
                        self.text_counter = 0
                        self.step += 1
            else:
                if int(self.text_counter) < len(self.text[i]):
                    self.text_counter += 0.05
                else:
                    if space:
                        #finish cutscene
                        self.cut_scene_running = False

        return self.cut_scene_running

    def draw(self, screen):
        for i in range (0, len(self.text)):
            if self.step == i:
                if self.step == 0 :
                    pygame.draw.rect(screen, (0,0,0), (0, 0, screen.get_width(), screen.get_height()))
                elif self.step == 1 or self.step == 2 or self.step == 3:
                    blit_bg_image(screen, 'cutscene1/bg1.png')
                elif self.step == 4 or self.step == 5:
                    blit_bg_image(screen, 'cutscene1/bg2.png')
                elif self.step == 6 or self.step == 7 or self.step == 8:
                    blit_bg_image(screen, 'cutscene1/bg3.png')
                else:
                    blit_bg_image(screen, 'cutscene1/bg4.jpeg')

                pygame.draw.rect(screen, (232, 207,166), (0, 550, screen.get_width(), 400))
                draw_text(screen, self.text[i][0:int(self.text_counter)], 35, (184,139,98), 50, 600)
       

class CutSceneTwo:
    def __init__(self):
        # Variables
        self.name = 'cutscene2'
        self.step = 0
        self.cut_scene_running = True

        # Dialogue
        self.setup()
        self.text_counter = 0

    def setup(self):
        self.text={}
        file_dialogue1 = open("story2.txt", "r")
        for index, item in enumerate(file_dialogue1.readlines()):
            self.text[index] = item

    def update(self):
        pressed = pygame.key.get_pressed()
        space = pressed[pygame.K_LCTRL]
        
        for i in range(0, len(self.text)):
            if self.step < len(self.text) - 1:
                if int(self.text_counter) < len(self.text[i]):
                    self.text_counter += 0.04
                else:
                    if space:
                        self.text_counter = 0
                        self.step += 1
            else:
                if int(self.text_counter) < len(self.text[i]):
                    self.text_counter += 0.04
                else:
                    if space:
                        #finish cutscene
                        self.cut_scene_running = False

        return self.cut_scene_running

    def draw(self, screen):
        for i in range (0, len(self.text)):
            if self.step == i:
                if self.step == 0 :
                    pygame.draw.rect(screen, (0,0,0), (0, 0, screen.get_width(), screen.get_height()))
                    pygame.draw.rect(screen, (232, 207,166), (0, 550, screen.get_width(), 400))
                    draw_text(screen, self.text[i][0:int(self.text_counter)], 35, (184,139,98), 50, 600)

                elif self.step == 1 or self.step == 4 or self.step == 5 or self.step == 6:
                    #dialogue box
                    blit_bg_image(screen, 'cutscene2/bg1.png')
                    draw_dialog_box(screen)
                    draw_chara(screen, 'cutscene2/emote1.png')
                    draw_text(screen, self.text[i][0:int(self.text_counter)], 35, (184,139,98), 275, 575)

                else:
                    blit_bg_image(screen, 'cutscene2/bg1.png')
                    pygame.draw.rect(screen, (232, 207,166), (0, 550, screen.get_width(), 400))
                    draw_text(screen, self.text[i][0:int(self.text_counter)], 35, (184,139,98), 50, 600) 
                

class CutSceneThree:
    def __init__(self):
        # Variables
        self.name = 'cutscene3'
        self.step = 0
        self.cut_scene_running = True

        # Dialogue
        self.setup()
        self.text_counter = 0

    def setup(self):
        self.text={}
        file_dialogue1 = open("story3.txt", "r")
        for index, item in enumerate(file_dialogue1.readlines()):
            self.text[index] = item
            # if index == 0 or 1 or 2 or 3 or 5 or 7 or 9 or 11:
            #     self.text_Bunn[index] = item
            # else:
            #     self.text_Merchant[index] = item

    def update(self):
        pressed = pygame.key.get_pressed()
        space = pressed[pygame.K_LCTRL]
        
        for i in range(0, len(self.text)):
            if self.step < len(self.text) - 1:
                if int(self.text_counter) < len(self.text[i]):
                    self.text_counter += 0.03
                else:
                    if space:
                        self.text_counter = 0
                        self.step += 1
            else:
                if int(self.text_counter) < len(self.text[i]):
                    self.text_counter += 0.03
                else:
                    if space:
                        #finish cutscene
                        self.cut_scene_running = False

        return self.cut_scene_running

    def draw(self, screen):
        for i in range (0, len(self.text)):
            if self.step == i:
                if self.step == 0 :
                    pygame.draw.rect(screen, (0,0,0), (0, 0, screen.get_width(), screen.get_height()))
                    pygame.draw.rect(screen, (232, 207,166), (0, 550, screen.get_width(), 400))
                    draw_text(screen, self.text[i][0:int(self.text_counter)], 35, (184,139,98), 50, 600)

                elif self.step == 5 or self.step == 12:
                    blit_bg_image(screen, 'cutscene3/bg1.png')
                    pygame.draw.rect(screen, (232, 207,166), (0, 550, screen.get_width(), 400))
                    draw_text(screen, self.text[i][0:int(self.text_counter)], 35, (184,139,98), 50, 600)
                
                else:
                    #dialogue box
                    blit_bg_image(screen, 'cutscene3/bg1.png')
                    draw_dialog_box(screen)
                    draw_text(screen, self.text[i][0:int(self.text_counter)], 35, (184,139,98), 275, 575)

                    if self.step == 1 or self.step == 2: draw_chara(screen, 'cutscene3/emote1.png')
                    elif self.step == 4: draw_chara(screen, 'cutscene3/emote2.png')
                    elif self.step == 9 or self.step == 10: draw_chara(screen, 'cutscene3/emote3.png')
                    else: draw_chara(screen, 'cutscene3/emote4.png')


class CutSceneFour:
    def __init__(self):
        # Variables
        self.name = 'cutscene4'
        self.step = 0
        self.cut_scene_running = True

        # Dialogue
        self.setup()
        self.text_counter = 0

    def setup(self):
        self.text={}
        file_dialogue1 = open("story4.txt", "r")
        for index, item in enumerate(file_dialogue1.readlines()):
            self.text[index] = item
            # if index == 0 or 1 or 2 or 3 or 5 or 7 or 9 or 11:
            #     self.text_Bunn[index] = item
            # else:
            #     self.text_Merchant[index] = item

    def update(self):
        pressed = pygame.key.get_pressed()
        space = pressed[pygame.K_LCTRL]
        
        for i in range(0, len(self.text)):
            if self.step < len(self.text) - 1:
                if int(self.text_counter) < len(self.text[i]):
                    self.text_counter += 0.04
                else:
                    if space:
                        self.text_counter = 0
                        self.step += 1
            else:
                if int(self.text_counter) < len(self.text[i]):
                    self.text_counter += 0.04
                else:
                    if space:
                        #finish cutscene
                        self.cut_scene_running = False

        return self.cut_scene_running

    def draw(self, screen):
        for i in range (0, len(self.text)):
            if self.step == i:
                if self.step == 0 :
                    pygame.draw.rect(screen, (0,0,0), (0, 0, screen.get_width(), screen.get_height()))

                else:
                    blit_bg_image(screen, 'cutscene4/bg1.png')
                    if self.step == 5 or self.step == 6 or self.step == 7:
                        letter_grandpa_surf = pygame.image.load('../graphics/dialogue/cutscene4/letter.png')
                        letter_grandpa_rect = letter_grandpa_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 90))
                        screen.blit(letter_grandpa_surf, letter_grandpa_rect)

                pygame.draw.rect(screen, (232, 207,166), (0, 550, screen.get_width(), 400))
                draw_text(screen, self.text[i][0:int(self.text_counter)], 35, (184,139,98), 50, 600)


class CutSceneManager:
    def __init__(self, screen):
        self.cut_scenes_complete = []
        self.cut_scene = None
        self.cut_scene_running = False

        # Drawing variables
        self.screen = screen

    def start_cut_scene(self, cut_scene):
        if cut_scene.name not in self.cut_scenes_complete: 
            self.cut_scenes_complete.append(cut_scene.name)             
            self.cut_scene = cut_scene
            self.cut_scene_running = True

    def end_cut_scene(self):
        self.cut_scene = None
        self.cut_scene_running = False

    def update(self):
        if self.cut_scene_running:
            self.cut_scene_running = self.cut_scene.update()
        else:
            self.end_cut_scene()

    def draw(self):
        if self.cut_scene_running:
            self.cut_scene.draw(self.screen)