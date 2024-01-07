import pygame
from game_settings import *
from pytmx.util_pygame import load_pygame
from support import import_folder, import_folder_dict
from random import choice

class Plant(pygame.sprite.Sprite):
    def __init__(self, plant_type, groups, soil, check_watered):
        #the basic setup
        super().__init__(groups)
        self.plant_type = plant_type
        self.frames = import_folder(f'../graphics/fruit/{plant_type}') #list of surfaces based on the plant type
        self.soil = soil 
        self.check_watered = check_watered

        #the plant growth
        self.age = 0
        self.max_age = len(self.frames) - 1
        self.grow_speed = GROW_SPEED[plant_type]
        self.harvestable = False #plant's is not harvestable by default

        #animation
        self.image = self.frames[self.age] #the image depends on the age of the plant
        self.y_offset = -16 if plant_type == 'corn' else -8 #y offset of the plant
        self.rect = self.image.get_rect(midbottom = soil.rect.midbottom + pygame.math.Vector2(0, self.y_offset))
        self.z = LAYERS['house bottom']

    def grow(self):
        #if it is watered, then age of the plant will be added by the grow speed
        if self.check_watered(self.rect.center):
            self.age += self.grow_speed

            #the layer of a grown plant (not a seed) is in main, so player can stand behinds them
            if int(self.age) > 0: 
                self.z = LAYERS['main']

            #if age is greater or equal to max age, then the plant is harvestable
            if self.age >= self.max_age:
                self.age = self.max_age
                self.harvestable = True

            #update the image based on the growth of the plant
            self.image = self.frames[int(self.age)]
            self.rect = self.image.get_rect(midbottom = self.soil.rect.midbottom + pygame.math.Vector2(0, self.y_offset))


class SoilTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        #image, rect, and layer for soiltile
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = LAYERS['soil']


class WaterTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        #image, rect, and layer for water on top of the soil tile
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = LAYERS['soil water']


class SoilLayer:
    def __init__(self, all_sprites, collision_sprites):
        #sprite groups
        self.all_sprites = all_sprites
        self.soil_sprites = pygame.sprite.Group()
        self.water_soil_sprites = pygame.sprite.Group()
        self.plant_sprites = pygame.sprite.Group()
        self.collision_sprites = collision_sprites

        #graphics
        self.soil_surfs = import_folder_dict('../graphics/soil')
        self.water_soil_surfs = import_folder('../graphics/soil_water')

        #create tiles that can be tiled as soil
        self.create_soil_grid()
        self.create_hit_rects()

        #sound
        #hoe sound for tilling soils
        self.hoe_sound = pygame.mixer.Sound('../audio/hoe.mp3')
        self.hoe_sound.set_volume(0.5)
        #plant sound for planting seeds
        self.plant_sound = pygame.mixer.Sound('../audio/plant.mp3')
   
    def create_soil_grid(self):
        #load the ground image and get the size of it
        ground = pygame.image.load('../graphics/world/ground.png')
        h_tiles = ground.get_width() // TILE_SIZE
        v_tiles = ground.get_height() // TILE_SIZE
        
        #list for each individual cell (tile) inside the col in horizontal tiles and row in vertical tiles
        self.grid = [[[]for col in range(h_tiles)] for row in range(v_tiles)]
        
        #if the cell is farmable, then the list for that cell will contain a F
        for x, y, _ in load_pygame('../data/map.tmx').get_layer_by_name('Farmable').tiles():
            self.grid[y][x].append('F')

    def create_hit_rects(self):
        self.hit_rects = []
        #if the cell contains F, then create a rect based on it and append it as hit rect
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'F' in cell:
                    x = index_col * TILE_SIZE
                    y = index_row * TILE_SIZE
                    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    self.hit_rects.append(rect)

    def get_hit(self, point):
        #for every rect in hit_rects
        for rect in self.hit_rects:
            #if rect collides with player's hoe target position
            if rect.collidepoint(point):
                self.hoe_sound.play()
                x = rect.x // TILE_SIZE
                y = rect.y // TILE_SIZE

                #if it's farmable and it's tilled, then the tile wiill contain X
                #and create a soil tile
                if 'F' in self.grid[y][x]:
                    self.grid[y][x].append('X')
                    self.create_soil_tiles()

                    #if it's raining, then tiles that contain X will be watered
                    #and there is water tile above them
                    if self.raining:
                        self.water_all()

    def create_soil_tiles(self):
        #draw all the soil tiles together, so that when a soil is 
        #tilled next to a tilled tile, then the tiles will be connected
        self.soil_sprites.empty() #empty the soil sprites, so we can create it all together
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                #if the soil is plantable or already tilled
                if 'X' in cell:
                    #tile options (are there any tilled soil on every positions of the tile)
                    top = 'X' in self.grid[index_row -1][index_col]
                    bottom = 'X' in self.grid[index_row + 1][index_col]
                    right = 'X' in row[index_col + 1]
                    left = 'X' in row[index_col - 1]

                    tile_type = 'o' #original type of tile if it's not connected to other tiles

                    #if the tile is connected to other tiles, then change the tile image
                    #connected to all sides
                    if all((top, bottom, right, left)): tile_type = 'x'

                    #connected to horizontal sides
                    if left and not any ((top, bottom, right)): tile_type = 'r' #left only
                    if right and not any ((top, bottom, left)): tile_type = 'l' #right only
                    if left and right and not any ((top, bottom)): tile_type = 'lr' #left and right

                    #connected to vertical sides
                    if top and not any ((right, bottom, left)): tile_type = 'b' #top only
                    if bottom and not any ((top, right, left)): tile_type = 't' #bottom only
                    if top and bottom and not any ((left, right)): tile_type = 'tb' #top and bottom

                    #connected to corners sides (L shape)
                    if left and bottom and not any ((top, right)): tile_type = 'tr' #bottom and left 
                    if right and bottom and not any ((top, left)): tile_type = 'tl' #right and bottom
                    if left and top and not any ((bottom, right)): tile_type = 'br' #left and top
                    if right and top and not any ((bottom, left)): tile_type = 'bl' #right and top

                    #connected to three sides/T shapes
                    if all((top, bottom, right)) and not left: tile_type = 'tbr' #top, bottom, right
                    if all((top, bottom, left)) and not right: tile_type = 'tbl' #top, bottom, left
                    if all((top, left, right)) and not bottom: tile_type = 'lrb' #top, left, right
                    if all((left, bottom, right)) and not top: tile_type = 'lrt' #left, bottom, right

                    #create the soiltile
                    SoilTile(
                        pos = (index_col * TILE_SIZE, index_row * TILE_SIZE), 
                        surf = self.soil_surfs[tile_type], 
                        groups = [self.all_sprites, self.soil_sprites])
                    
    def water(self, point):
        #for every soil tile
        for soil_sprite in self.soil_sprites.sprites():
            #if soil tile collides with water can's target pos
            if soil_sprite.rect.collidepoint(point):
                #the soil is watered, then append 'W' in the list
                x = soil_sprite.rect.x // TILE_SIZE
                y = soil_sprite.rect.y // TILE_SIZE
                self.grid[y][x].append('W')
                soil_pos = soil_sprite.rect.topleft

                #create a water tile above the soil tile
                WaterTile(
                    pos = soil_pos,
                    surf = choice(self.water_soil_surfs),
                    groups = [self.all_sprites, self.water_soil_sprites]
                )
    
    def water_all(self):
        #for every tile
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                #if the tile is plantable, but is not watered, then water it
                if 'X' in cell and 'W' not in cell:
                    cell.append('W')

                    #create watertile above the soiltile
                    WaterTile(
                        pos = (index_col * TILE_SIZE, index_row * TILE_SIZE),
                        surf = choice(self.water_soil_surfs),
                        groups = [self.all_sprites, self.water_soil_sprites]
                    )

    def remove_water(self):
        #destroy all the water sprites
        for sprite in self.water_soil_sprites.sprites():
            sprite.kill()
        
        #empty the cell from W if there is W
        for row in self.grid:
            for cell in row:
                if 'W' in cell:
                    cell.remove('W')

    def check_watered(self, pos):
        #if W is in the cell, then return True
        x = pos[0] // TILE_SIZE
        y = pos[1] // TILE_SIZE
        cell = self.grid[y][x]
        is_watered = 'W' in cell
        return is_watered

    def plant_seed(self, target_pos, seed):
        #if the player plant seeds in the soil tile, then the soil tile will contains the code P
        #means that the soil is planted
        for soil_sprite in self.soil_sprites.sprites():
            #if soil tile collides with the target position
            if soil_sprite.rect.collidepoint(target_pos):
                self.plant_sound.play()
                x = soil_sprite.rect.x // TILE_SIZE
                y = soil_sprite.rect.y // TILE_SIZE

                #create plant object only if the soil is not planted before
                if 'P' not in self.grid[y][x]:
                    self.grid[y][x].append('P')
                    Plant(
                        plant_type = seed,
                        groups = [self.all_sprites, self.plant_sprites, self.collision_sprites],
                        soil = soil_sprite,
                        check_watered = self.check_watered
                    )

    def check_plantable(self, target_pos):
        for soil_sprite in self.soil_sprites.sprites():
            if soil_sprite.rect.collidepoint(target_pos):
                x = soil_sprite.rect.x // TILE_SIZE
                y = soil_sprite.rect.y // TILE_SIZE

                #if plantable and still no plant then return true and the seed can be planted
                #if not then, the seed cannot be planted and it doesnt deduct the seed amount
                if 'X' in self.grid[y][x] and 'P' not in self.grid[y][x]: return True

        return False

    def update_plants(self):
        #grow every plant
        for plant in self.plant_sprites.sprites():
            plant.grow()
