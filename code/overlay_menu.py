import pygame
from game_settings import *

class Overlay_Menu:
    def __init__(self, player, toggle_menu):
        #basic setup
        self.player = player
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('../font/Rubik-Bold.ttf', 40)
        self.font2 = pygame.font.Font('../font/Rubik-SemiBold.ttf', 25)

        #graphics
        self.width = 800
        self.height = 650

        #toggle
        self.toggle_menu = toggle_menu

        self.setup()

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_o]:
            self.toggle_menu()

    def setup(self):
        self.text_surfs = []

        for key, desc in KEYBOARD_KEYS.items():
            text_surf = self.font2.render(f"{key} : {desc}", False, (184,139,98))
            self.text_surfs.append(text_surf)

    def show(self):
        #background
        self.menu_top = SCREEN_HEIGHT / 2 - self.height / 2
        self.main_rect = pygame.Rect(SCREEN_WIDTH/2 - self.width/2, self.menu_top, self.width, self.height)
        pygame.draw.rect(self.display_surface, (232, 207,166), self.main_rect)

        #text
        text_surf = self.font.render("KEYBOARD USE", False, 'BLACK')
        text_rect = text_surf.get_rect(midtop = (self.main_rect.centerx, self.main_rect.top+10))
        self.display_surface.blit(text_surf, text_rect)

        space = 10
        for item_surf in self.text_surfs:
            item_rect = item_surf.get_rect(topleft = (self.main_rect.left+40, self.main_rect.top + 80 + space))
            self.display_surface.blit(item_surf, item_rect)
            space += 40

    def update(self):
        self.input() 
        self.show()
    

class Inventory:
    def __init__(self, player, toggle_menu):
        #basic setup
        self.player = player
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('../font/Rubik-Bold.ttf', 40)
        self.font2 = pygame.font.Font('../font/Rubik-SemiBold.ttf', 25)

        #graphics
        self.width = 640
        self.height = 360

        #toggle
        self.toggle_menu = toggle_menu

        self.setup()

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_o]:
            self.toggle_menu()

    def setup(self):
        self.text_surfs = []

        for key, amount in self.player.item_inventory.items():
            text_surf = self.font2.render(f"{key} : {amount}", False, (184,139,98))
            self.text_surfs.append(text_surf)

        for key, amount in self.player.seed_inventory.items():
            text_surf = self.font2.render(f"{key} seed : {amount}", False, (184,139,98))
            self.text_surfs.append(text_surf)

    def show(self):
        #background
        self.menu_top = SCREEN_HEIGHT / 2 - self.height / 2
        self.main_rect = pygame.Rect(SCREEN_WIDTH/2 - self.width/2, self.menu_top, self.width, self.height)
        pygame.draw.rect(self.display_surface, (244,231,196), self.main_rect)

        #text
        text_surf = self.font.render("INVENTORY", False, 'BLACK')
        text_rect = text_surf.get_rect(midtop = (self.main_rect.centerx, self.main_rect.top+10))
        self.display_surface.blit(text_surf, text_rect)

        space = 10
        for item_surf in self.text_surfs:
            item_rect = item_surf.get_rect(topleft = (self.main_rect.left+40, self.main_rect.top + 80 + space))
            self.display_surface.blit(item_surf, item_rect)
            space += 40

    def update(self):
        self.input() 
        self.show()
    
