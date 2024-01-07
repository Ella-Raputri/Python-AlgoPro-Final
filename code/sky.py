import pygame
from game_settings import *
from support import import_folder
from random import randint, choice
from sprites import Generic

class Sky:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        #full surface of the sky
        self.full_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        #starts with white color and ends with rather blueish color
        self.start_color = [255, 255, 255]
        self.end_color = (38, 101, 189)

    def display (self, dt):
        #change the color if the start color is greater than the end color
        color_change = 2
        for index, value in enumerate(self.end_color):
            if self.start_color[index] > value:
                self.start_color[index] -= color_change * dt

        #fill the full surface with the start color that change over time
        self.full_surf.fill(self.start_color)
        #blit it with special blend multiply
        self.display_surface.blit(self.full_surf, (0,0), special_flags=pygame.BLEND_RGBA_MULT)

class Drop(Generic):
    def __init__(self, surf, pos, moving, groups, z):
        #general setup
        super().__init__(pos, surf, groups, z)
        self.lifetime = randint(400,500)
        self.start_time = pygame.time.get_ticks()
        
        #moving raindrop
        self.moving = moving
        if self.moving:
            #if the raindrop is moving, then set the position, direction, and speed
            self.pos = pygame.math.Vector2(self.rect.topleft)
            self.direction = pygame.math.Vector2(-3,4)
            self.speed = randint(200,250)

    def update(self, dt):
        #movement
        if self.moving:
            #update the position
            self.pos += self.direction * self.speed * dt
            self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        #timer
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            #if it's duration already greater than it's lifetime then kill it
            self.kill()

class Rain:
    def __init__(self, all_sprites):
        self.all_sprites = all_sprites
        #list of rain drops images
        self.rain_drops = import_folder('../graphics/rain/drops')
        #list of rain floor images
        self.rain_floor = import_folder('../graphics/rain/floor')

        #size of the map
        self.floor_width, self.floor_height = pygame.image.load('../graphics/world/ground.png').get_size()
    
    def create_floor(self):
        #create rain floors
        Drop(
            surf = choice(self.rain_floor), 
            #the surface is randomized from the rain_floor surfaces
            pos = (randint(0, self.floor_width), randint(0, self.floor_height)), 
            #the position is randomized based on the size of the map
            moving = False, #it is not moving because it is rain floor
            groups = self.all_sprites, 
            z = LAYERS['rain floor'])

    def create_drops(self):
        #create rain drops
        Drop(
            surf = choice(self.rain_drops), 
            #the surface is randomized from the rain_drops surfaces
            pos = (randint(0, self.floor_width), randint(0, self.floor_height)), 
            #the position is randomized based on the size of the map
            moving = True, #rain drops is moving from topleft
            groups = self.all_sprites, 
            z = LAYERS['rain drops'])

    def update(self):
        #create rain floors and drops if it's raining
        self.create_floor()
        self.create_drops()