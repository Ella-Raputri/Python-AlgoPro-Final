import pygame, math
from game_settings import *
from support import *

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
        self.font = pygame.font.Font('../font/LycheeSoda.ttf', 40)
        self.font_amount = pygame.font.Font('../font/LycheeSoda.ttf', 28)

        #graphics
        self.width = 480
        self.height = 480
        self.vertical_space = 80
        self.horizontal_space = 30
        self.padding = 10

        #toggle
        self.toggle_menu = toggle_menu

        #entries
        self.list_items = list(self.player.item_inventory.keys()) + list(self.player.seed_inventory.keys()) + list(self.player.other_inventory.keys())
        path = '../graphics/inventory'
        self.list_images = import_folder(f'{path}/item_inventory') + import_folder(f'{path}/seed_inventory') + import_folder(f'{path}/other_inventory')

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_o]:
            self.toggle_menu()

    def blit_image(self, row, column):
        vert_space = self.vertical_space + (1.8 * row * self.vertical_space)
        horizontal_space = self.padding + self.horizontal_space + (5 * column * self.horizontal_space)

        image_surf = self.list_images[(row*3)+column]
        image_rect = image_surf.get_rect(topleft = (self.main_rect.left+ horizontal_space, self.main_rect.top + vert_space))
        pygame.draw.rect(self.display_surface, (232, 207,166), image_rect)
        self.display_surface.blit(image_surf, image_rect)

    def show(self):
        #background
        self.menu_top = SCREEN_HEIGHT / 2 - self.height / 2
        self.main_rect = pygame.Rect(SCREEN_WIDTH/2 - self.width/2, self.menu_top, self.width, self.height)
        pygame.draw.rect(self.display_surface, (244,231,196), self.main_rect)
        
        #text header
        text_surf = self.font.render("INVENTORY", False, 'BLACK')
        text_rect = text_surf.get_rect(midtop = (self.main_rect.centerx, self.main_rect.top+ self.padding))
        self.display_surface.blit(text_surf, text_rect)

        #image
        for row in range (0, (len(self.list_images) // 3)):
            for column in range (0, 3):
                self.blit_image(row, column)
        self.blit_image(2, 0)
        
    def show_amount(self, row, column, text, amount):
        vert_space = 60 + self.vertical_space + (1.8 * row * self.vertical_space)
        horizontal_space = self.padding + self.horizontal_space + (5 * column * self.horizontal_space)

        amount_surf = self.font_amount.render(f'{text} : {amount}', False, 'Black')
        amount_rect = amount_surf.get_rect(topleft = (self.main_rect.left+ horizontal_space, self.main_rect.top + vert_space))
        self.display_surface.blit(amount_surf, amount_rect)

    def update(self):
        self.input() 
        self.show()

        #showing amount
        amount_list = list(self.player.item_inventory.values()) + list(self.player.seed_inventory.values()) + list(self.player.other_inventory.values())
        for row in range (0, (len(self.list_items) // 3)):
            for column in range (0, 3):
                amount = amount_list[(row*3) + column]
                text = self.list_items[(row*3) + column]
                self.show_amount(row, column, text, amount)

        self.show_amount(2, 0, self.list_items[6], amount_list[6])
    
