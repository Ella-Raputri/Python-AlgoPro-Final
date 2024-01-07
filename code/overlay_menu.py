import pygame
from game_settings import *
from support import import_folder

class Overlay_Menu:
    def __init__(self, player, toggle_menu):
        #basic setup
        self.player = player
        self.display_surface = pygame.display.get_surface()
        #font
        self.font = pygame.font.Font('../font/Rubik-Bold.ttf', 35)
        self.font2 = pygame.font.Font('../font/Rubik-SemiBold.ttf', 25)

        #graphics
        self.width = 800
        self.height = 650

        #toggle
        self.toggle_menu = toggle_menu
        self.setup()

    def input(self):
        #check if key get pressed
        keys = pygame.key.get_pressed()
        #if player press O, toggle help menu
        if keys[pygame.K_o]:
            self.toggle_menu()

    def setup(self):
        self.text_surfs = []
        #for every key and its description, append it to text_surfs
        for key, desc in KEYBOARD_KEYS.items():
            text_surf = self.font2.render(f"{key} : {desc}", False, GAME_COLOR['text'])
            self.text_surfs.append(text_surf)

    def show(self):
        #the main background for help menu
        self.menu_top = SCREEN_HEIGHT / 2 - self.height / 2
        self.main_rect = pygame.Rect(SCREEN_WIDTH/2 - self.width/2, self.menu_top, self.width, self.height)
        pygame.draw.rect(self.display_surface, GAME_COLOR['dialogue box'], self.main_rect)

        #the topic text for the help menu
        text_surf = self.font.render("KEYBOARD SHORTCUT", False, 'BLACK')
        text_rect = text_surf.get_rect(midtop = (self.main_rect.centerx, self.main_rect.top+10))
        self.display_surface.blit(text_surf, text_rect)

        space = 10
        for item_index, item_surf in enumerate(self.text_surfs):
            #blit the key and description text
            item_rect = item_surf.get_rect(topleft = (self.main_rect.left+40, self.main_rect.top + 60 + space))
            self.display_surface.blit(item_surf, item_rect)
            space += 35 #every key's description has about 35 px space from each other

            #under all the key and description, blit this sentence
            if item_index == len(self.text_surfs) - 1:   
                instruction_surf = self.font2.render('Play the story to get more money and a decoration', False, GAME_COLOR['text'])
                instruction_rect = instruction_surf.get_rect(topleft = (self.main_rect.left+40, self.main_rect.top + 60 + space))
                self.display_surface.blit(instruction_surf, instruction_rect)

    def update(self):
        #update the menu based on player's input
        self.input() 
        self.show() #show the menu
    

class Inventory:
    def __init__(self, player, toggle_menu):
        #basic setup
        self.player = player
        self.display_surface = pygame.display.get_surface()
        #font
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
        #list of the items
        self.list_items = list(self.player.item_inventory.keys()) \
            + list(self.player.seed_inventory.keys()) + list(self.player.other_inventory.keys())
        path = '../graphics/inventory'

        #list of the item images
        self.list_images = import_folder(f'{path}/item_inventory') + \
            import_folder(f'{path}/seed_inventory') + import_folder(f'{path}/other_inventory')

    def input(self):
        #check if there are any keys got pressed
        keys = pygame.key.get_pressed()

        #if player press O, toggle inventory
        if keys[pygame.K_o]:
            self.toggle_menu()

    def blit_image(self, row, column):
        #the formula for counting the vertical space and horizontal space for each item
        #each item vertical's and horizontal space depends on what row and column that they are in
        vert_space = self.vertical_space + (1.8 * row * self.vertical_space)
        horizontal_space = self.padding + self.horizontal_space + (5 * column * self.horizontal_space)

        #accesing the image surf and get the image rect
        image_surf = self.list_images[(row*3)+column]
        image_rect = image_surf.get_rect(topleft = (self.main_rect.left+ horizontal_space, self.main_rect.top + vert_space))
        #draw a darker brown rect as the background of the item's image
        pygame.draw.rect(self.display_surface, GAME_COLOR['dialogue box'], image_rect)
        self.display_surface.blit(image_surf, image_rect)

    def show(self):
        #background for the inventory
        self.menu_top = SCREEN_HEIGHT / 2 - self.height / 2
        self.main_rect = pygame.Rect(SCREEN_WIDTH/2 - self.width/2, self.menu_top, self.width, self.height)
        pygame.draw.rect(self.display_surface, GAME_COLOR['inventory'], self.main_rect)
        
        #text header
        text_surf = self.font.render("INVENTORY", False, 'BLACK')
        text_rect = text_surf.get_rect(midtop = (self.main_rect.centerx, self.main_rect.top+ self.padding))
        self.display_surface.blit(text_surf, text_rect)

        #money 
        text_surf = self.font.render(f'Money: ${self.player.money}', False, 'Black')
        text_rect = text_surf.get_rect(midtop = (self.main_rect.centerx, self.main_rect.top - (5*self.padding)))
        #the white background for the money text
        pygame.draw.rect(self.display_surface, 'White', text_rect.inflate(10,10), 0, 5)
        self.display_surface.blit(text_surf, text_rect)

        #blit all image on their respective position
        for row in range (0, (len(self.list_images) // 3)):
            for column in range (0, 3):
                self.blit_image(row, column)
        #blit the last image because it is not included in the for loop
        self.blit_image(2, 0)
        
    def show_amount(self, row, column, text, amount):
        #the amount text vertical and horizontal space also depens on the row and column which they are in
        vert_space = 60 + self.vertical_space + (1.8 * row * self.vertical_space)
        horizontal_space = self.padding + self.horizontal_space + (5 * column * self.horizontal_space)

        #generate and blit the amount text
        amount_surf = self.font_amount.render(f'{text} : {amount}', False, 'Black')
        amount_rect = amount_surf.get_rect(topleft = (self.main_rect.left+ horizontal_space, self.main_rect.top + vert_space))
        self.display_surface.blit(amount_surf, amount_rect)

    def update(self):
        self.input() #update based on player's input
        self.show() #show inventory

        #showing amount based on the most updated version of player's inventory
        amount_list = list(self.player.item_inventory.values()) + \
            list(self.player.seed_inventory.values()) + list(self.player.other_inventory.values())
        for row in range (0, (len(self.list_items) // 3)):
            for column in range (0, 3):
                amount = amount_list[(row*3) + column]
                text = self.list_items[(row*3) + column]
                self.show_amount(row, column, text, amount)

        #show amount for grass because it is not included in the for loop
        self.show_amount(2, 0, self.list_items[6], amount_list[6])
    
