import pygame
from game_settings import *
from support import Timer

class Menu:
    def __init__(self, player, toggle_menu):
        #basic setup
        self.player = player
        self.toggle_menu = toggle_menu
        self.display_surface = pygame.display.get_surface() 
        self.font = pygame.font.Font('../font/LycheeSoda.ttf', 30)

        #graphics
        self.width = 400
        self.space = 10
        self.padding = 8

        #entries
        self.options = list(self.player.item_inventory.keys()) + list(self.player.seed_inventory.keys()) + list(self.player.other_inventory.keys())
        self.sell_border = len(self.player.item_inventory) - 1 #to determine which item can be bought and can be sold
        self.setup()

        #movement
        self.index = 0 #starts from the top one
        self.timer = Timer(200) #used to normalize movement

        #sound
        #when player sells something
        self.sell_sound = pygame.mixer.Sound('../audio/sell.mp3')
        self.sell_sound.set_volume(0.6)
        #when player buys something
        self.buy_sound = pygame.mixer.Sound('../audio/buy.mp3')
        self.buy_sound.set_volume(0.6)
    
    def display_money(self):
        #render font and get its rect to display the money text
        text_surf = self.font.render(f'Money: ${self.player.money}', False, 'Black')
        text_rect = text_surf.get_rect(midbottom= (SCREEN_WIDTH/2, SCREEN_HEIGHT -600))
        #the background of the text is white
        pygame.draw.rect(self.display_surface, 'White', text_rect.inflate(10,10), 0, 5)
        self.display_surface.blit(text_surf, text_rect)

    def setup(self):
        #all prices of the item regardless it's sale prices or purchase prices
        ALL_PRICES = []
        for price in SALE_PRICES.values():
            ALL_PRICES.append(price)
        for price in PURCHASE_PRICES.values():
            ALL_PRICES.append(price)

        #create the text surfaces
        self.text_surfs = []
        self.total_height = 0
        i = 0
        #for every item
        for item in self.options:
            #render the name and the price of each item, append it to the text_surfs list
            text_surf = self.font.render(F'{item} (${ALL_PRICES[i]})', False, 'Black')
            self.text_surfs.append(text_surf)
            #calculate the total height of the menu
            self.total_height += text_surf.get_height() + (self.padding * 2)
            #go to next item's price in ALL_PRICES
            i += 1

        #calculate the total height of the menu
        self.total_height += (len(self.text_surfs) - 1) * self.space
        #set the position of the top of the menu
        self.menu_top = SCREEN_HEIGHT / 2 - self.total_height / 2
        #the menu rect 
        self.main_rect = pygame.Rect(SCREEN_WIDTH/2 - self.width/2, self.menu_top, self.width, self.total_height)

        #buy and sell text surface
        self.buy_text = self.font.render('buy', False, 'darkred')
        self.sell_text = self.font.render('sell', False, 'chartreuse3')

    def input(self):
        #check if key is pressed
        keys = pygame.key.get_pressed()
        self.timer.update()

        #if player press o, then toggle shop
        if keys[pygame.K_o]:
            self.toggle_menu()
        
        #if the timer for the movement is not active
        if not self.timer.active:
            #if player press arrow up, then go to the item above
            if keys[pygame.K_UP]:
                self.index -= 1
                self.timer.activate() #activate timer
            #if player press arrow down, then go to the item below
            if keys[pygame.K_DOWN]:
                self.index += 1
                self.timer.activate() #activate timer
            
            if keys[pygame.K_SPACE]:
                self.timer.activate()
                #get item 
                current_item = self.options[self.index]

                #sell item if the item is greater than 0
                if self.index <= self.sell_border:
                    if self.player.item_inventory[current_item] > 0:
                        self.sell_sound.play()
                        #deduct player's item amount and add player money
                        self.player.item_inventory[current_item] -= 1
                        self.player.money += SALE_PRICES[current_item]
               
                #buy item if the money is enough
                else:
                    if self.player.money >= PURCHASE_PRICES[current_item]:
                        self.buy_sound.play()
                        #if it's a grass, then add grass item by 1
                        if current_item == 'grass':
                            self.player.other_inventory[current_item] += 1
                        #else, add seed amount based on the plant type
                        else:
                            self.player.seed_inventory[current_item] += 1
                        #deducts player money
                        self.player.money -= PURCHASE_PRICES[current_item]
                        
        
        #if player press the up arrow key while in the first entry, then the
        #active entry goes to the last entry
        if self.index < 0:
            self.index = len(self.options) - 1
        #if player press the down arrow key while in the last entry, then the
        #active entry goes to the first entry
        if self.index > len(self.options)-1:
            self.index = 0

    def show_entries(self, text_surf, amount, top, selected):
        #background surface (white) for each entry
        bg_height = text_surf.get_height() + (self.padding * 2)
        bg_rect = pygame.Rect(self.main_rect.left, top, self.width, bg_height)
        pygame.draw.rect(self.display_surface, 'White', bg_rect, 0, 5)

        #text surface
        text_rect = text_surf.get_rect(midleft = (self.main_rect.left + 20, bg_rect.centery))
        self.display_surface.blit(text_surf, text_rect)

        #amount surface
        amount_surf = self.font.render(str(amount), False, 'Black')
        amount_rect = amount_surf.get_rect(midright = (self.main_rect.right - 20, bg_rect.centery))
        self.display_surface.blit(amount_surf, amount_rect)

        #selected
        if selected:

            pygame.draw.rect(self.display_surface, 'black', bg_rect, 4, 4)
            if self.index <= self.sell_border: #sell item
                pos_rect = self.sell_text.get_rect(midleft = (self.main_rect.left + 200, bg_rect.centery))
                self.display_surface.blit(self.sell_text, pos_rect)
            else:
                pos_rect = self.buy_text.get_rect(midleft = (self.main_rect.left + 200, bg_rect.centery))
                self.display_surface.blit(self.buy_text, pos_rect)

    def update(self):
        self.input() #update based on player's input
        self.display_money() #display money

        #for every text index and text surface in text surfs
        for text_index, text_surf in enumerate(self.text_surfs):
            #top of the background rect
            top = self.main_rect.top + text_index * (text_surf.get_height() + (self.padding *2) + self.space)
            #the amount of each item
            amount_list = list(self.player.item_inventory.values()) + list(self.player.seed_inventory.values()) + list(self.player.other_inventory.values())
            amount = amount_list[text_index]
            self.show_entries(text_surf, amount, top, self.index == text_index)