import pygame

def draw_text(screen, text, size, color, x, y):
    font = pygame.font.Font('../font/LycheeSoda.ttf', size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

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
                if self.step == 0:
                    pygame.draw.rect(screen, 'black', screen.get_rect())
                else:
                    city_pict = pygame.image.load('../graphics/1890.jpg')
                    city_rect = city_pict.get_rect(topleft=(0,0))
                    screen.blit(city_pict, city_rect)
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
            if self.step == i: #275 for dialog box
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
            if self.step == i: #275 for dialog box
                draw_text(screen, self.text[i][0:int(self.text_counter)], 35, (184,139,98), 50, 600)


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
            if self.step == i: #275 for dialog box
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