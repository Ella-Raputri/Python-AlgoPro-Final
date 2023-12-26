import pygame
from game_settings import *
from support import *
from random import randint, choice
from sprites import Generic

class Sky:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.full_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.start_color = [255, 255, 255]
        self.end_color = (38, 101, 189)

    def display (self, dt):
        color_change = 2
        for index, value in enumerate(self.end_color):
            if self.start_color[index] > value:
                self.start_color[index] -= color_change * dt

        self.full_surf.fill(self.start_color)
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
            self.pos = pygame.math.Vector2(self.rect.topleft)
            self.direction = pygame.math.Vector2(-3,4)
            self.speed = randint(200,250)

    def update(self, dt):
        #movement
        if self.moving:
            self.pos += self.direction * self.speed * dt
            self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        #timer
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()

class Rain:
    def __init__(self, all_sprites):
        self.all_sprites = all_sprites
        self.rain_drops = import_folder('../graphics/rain/drops')
        self.rain_floor = import_folder('../graphics/rain/floor')

        self.floor_width, self.floor_height = pygame.image.load('../graphics/world/ground.png').get_size()
    
    def create_floor(self):
        Drop(
            surf = choice(self.rain_floor), 
            pos = (randint(0, self.floor_width), randint(0, self.floor_height)), 
            moving = False, 
            groups = self.all_sprites, 
            z = LAYERS['rain floor'])

    def create_drops(self):
        Drop(
            surf = choice(self.rain_drops), 
            pos = (randint(0, self.floor_width), randint(0, self.floor_height)), 
            moving = True, 
            groups = self.all_sprites, 
            z = LAYERS['rain drops'])

    def update(self):
        self.create_floor()
        self.create_drops()