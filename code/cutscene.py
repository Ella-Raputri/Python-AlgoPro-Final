import pygame
from game_settings import *

def draw_text(screen, text, size, color, x, y):
    #a function to draw the text on the screen, the font is all LycheeSoda
    font = pygame.font.Font('../font/LycheeSoda.ttf', size)

    #render fon to become text surface and sets its rect position as (x,y) from topleft 
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(topleft=(x,y))

    #blit the text on the screen
    screen.blit(text_surface, text_rect)

def blit_bg_image(screen, path):
    #get the background image surface and set its rect as (0,0)
    #because background image has to cover all of the screen
    bg_pict = pygame.image.load(f'../graphics/dialogue/{path}')
    bg_rect = bg_pict.get_rect(topleft=(0,0))
    #blit the image
    screen.blit(bg_pict, bg_rect)

def draw_chara(screen, path):
    #get the character image surface and set its rect as (65,510)
    #to fit in the dialogue box
    chara_surf = pygame.image.load((f'../graphics/dialogue/{path}'))
    chara_rect = chara_surf.get_rect(topleft=(65,510))
    #blit the chara avatar image
    screen.blit(chara_surf, chara_rect)

def draw_dialog_box(screen):
    #get the dialogue box image surface and set its rect to fit in the screen
    dialog_pict = pygame.image.load(f'../graphics/dialogue/dialog_box.png')
    dialog_rect = dialog_pict.get_rect(topleft=(0,450))
    #blit the dialogue box image
    screen.blit(dialog_pict, dialog_rect)


class CutSceneOne:
    def __init__(self):
        # Basic setup
        self.name = 'cutscene1' #cutscene's name
        self.step = 0 #on which scene now is the cutscene
        self.cut_scene_running = True #the status of the cutscene

        # Dialogue
        self.setup()
        # text counter is used to create the slide-right effect when playing the cutscene
        self.text_counter = 0

        # Sound when press LCtrl key to proceed the cutscene
        self.next_sound = pygame.mixer.Sound('../audio/cutscene.mp3')
        self.next_sound.set_volume(0.3)      

    def setup(self):
        # Append all lines in the story1 in the self.text dictionary
        self.text={}
        file_story1 = open("../story/story1.txt", "r")
        for index, item in enumerate(file_story1.readlines()):
            self.text[index] = item

    def update(self):
        #check if the LCtrl key get pressed or not
        pressed = pygame.key.get_pressed()
        lctrl = pressed[pygame.K_LCTRL]
        
        #for every lines of dialogue
        for i in range(0, len(self.text)):
            #if cutscene is not on the last line of dialogue
            if self.step < len(self.text) - 1:
                
                #if the text counter still shorter than amount of character
                #in the dialogue line, then add the text counter to provide the
                #slide-right effect of the text
                if int(self.text_counter) < len(self.text[i]):
                    self.text_counter += 0.05
                
                #if LCtrl is pressed, then play next sound, go to the next step
                #text counter becomes 0 again
                else:
                    if lctrl:
                        self.next_sound.play()
                        self.text_counter = 0
                        self.step += 1
            
            #if cutscene is on the last line of dialogue
            else:
                #the text animation slide-right effect
                if int(self.text_counter) < len(self.text[i]):
                    self.text_counter += 0.05
                else:
                    if lctrl:
                        #finish cutscene if LCtrl is pressed
                        self.cut_scene_running = False

        return self.cut_scene_running

    def draw(self, screen):
        #for every lines of dialogue
        for i in range (0, len(self.text)):
            if self.step == i:
                #if it is the first line, blit a black rect
                if self.step == 0 :
                    pygame.draw.rect(screen, (0,0,0), (0, 0, screen.get_width(), screen.get_height()))
                
                #blit background image based on the line's number
                elif self.step == 1 or self.step == 2 or self.step == 3:
                    blit_bg_image(screen, 'cutscene1/bg1.png')
                elif self.step == 4 or self.step == 5:
                    blit_bg_image(screen, 'cutscene1/bg2.png')
                elif self.step == 6 or self.step == 7 or self.step == 8:
                    blit_bg_image(screen, 'cutscene1/bg3.png')
                else:
                    blit_bg_image(screen, 'cutscene1/bg4.png')

                #draw the narrator brown rect on the screen
                pygame.draw.rect(screen, GAME_COLOR['dialogue box'], (0, 550, screen.get_width(), 400))
                #draw the dialogue line text
                draw_text(screen, self.text[i][0:int(self.text_counter)], 35, GAME_COLOR['text'], 50, 600)
       

class CutSceneTwo:
    def __init__(self):
        # Basic setup
        self.name = 'cutscene2' #cutscene's name
        self.step = 0 #on which scene now is the cutscene
        self.cut_scene_running = True #the status of the cutscene

        # Dialogue
        self.setup()
        # text counter is used to create the slide-right effect when playing the cutscene
        self.text_counter = 0

        # Sound when press LCtrl key to proceed the cutscene
        self.next_sound = pygame.mixer.Sound('../audio/cutscene.mp3')
        self.next_sound.set_volume(0.3)  

    def setup(self):
        # Append all lines in the story2 in the self.text dictionary
        self.text={}
        file_story2 = open("../story/story2.txt", "r")
        for index, item in enumerate(file_story2.readlines()):
            self.text[index] = item

    def update(self):
        #check if the LCtrl key get pressed or not
        pressed = pygame.key.get_pressed()
        lctrl = pressed[pygame.K_LCTRL]
        
        #for every lines of dialogue
        for i in range(0, len(self.text)):
            #if cutscene is not on the last line of dialogue
            if self.step < len(self.text) - 1:
                #the text animation slide-right effect
                if int(self.text_counter) < len(self.text[i]):
                    self.text_counter += 0.05
                else:
                    #if LCtrl is pressed, go to next scene
                    if lctrl:
                        self.next_sound.play()
                        self.text_counter = 0
                        self.step += 1
            #if cutscene is on the last line of dialogue
            else:
                #text slide-right animation
                if int(self.text_counter) < len(self.text[i]):
                    self.text_counter += 0.05
                else:
                    if lctrl:
                        #finish cutscene if LCtrl is pressed
                        self.cut_scene_running = False

        return self.cut_scene_running

    def draw(self, screen):
        #for every lines of dialogue
        for i in range (0, len(self.text)):
            if self.step == i:
                #if it is the first line, draw the narrator box rect, black background rect, and the text
                if self.step == 0 :
                    pygame.draw.rect(screen, (0,0,0), (0, 0, screen.get_width(), screen.get_height()))
                    pygame.draw.rect(screen, GAME_COLOR['dialogue box'], (0, 550, screen.get_width(), 400))
                    draw_text(screen, self.text[i][0:int(self.text_counter)], 35, GAME_COLOR['text'], 50, 600)
                
                #blit background image based on the line's number
                elif self.step == 1 or self.step == 4 or self.step == 5 or self.step == 6:
                    #if it is the 2nd, 5th, 6th, or 7th line
                    blit_bg_image(screen, 'cutscene2/bg1.png')
                    #draw the dialogue box, chara avatar, and text
                    draw_dialog_box(screen)
                    draw_chara(screen, 'cutscene2/emote1.png')
                    draw_text(screen, self.text[i][0:int(self.text_counter)], 35, GAME_COLOR['text'], 275, 575)

                else:
                    blit_bg_image(screen, 'cutscene2/bg1.png')
                    #draw the narrator box
                    pygame.draw.rect(screen, GAME_COLOR['dialogue box'], (0, 550, screen.get_width(), 400))
                    draw_text(screen, self.text[i][0:int(self.text_counter)], 35, GAME_COLOR['text'], 50, 600) 
                

class CutSceneThree:
    def __init__(self):
        # Basic setup
        self.name = 'cutscene3' #cutscene's name
        self.step = 0 #on which scene now is the cutscene
        self.cut_scene_running = True #the status of the cutscene

        # Dialogue
        self.setup()    
        self.text_counter = 0 #for slide-right text animation

        #sound effect when pressing LCtrl
        self.next_sound = pygame.mixer.Sound('../audio/cutscene.mp3')
        self.next_sound.set_volume(0.3)  

    def setup(self):
        # Append all lines in the story3 in the self.text dictionary
        self.text={}
        file_story3 = open("../story/story3.txt", "r")
        for index, item in enumerate(file_story3.readlines()):
            self.text[index] = item

    def update(self):
        #check if the LCtrl key get pressed or not
        pressed = pygame.key.get_pressed()
        lctrl = pressed[pygame.K_LCTRL]
        
        #for every lines of dialogue
        for i in range(0, len(self.text)):
            #if cutscene is not on the last line of dialogue
            if self.step < len(self.text) - 1:
                #text slide-right animation
                if int(self.text_counter) < len(self.text[i]):
                    self.text_counter += 0.05
                else:
                    #go to next step
                    if lctrl:
                        self.next_sound.play()
                        self.text_counter = 0
                        self.step += 1

            #if cutscene is on the last line of dialogue
            else:
                #text slide-right animation
                if int(self.text_counter) < len(self.text[i]):
                    self.text_counter += 0.05
                else:
                    if lctrl:
                        #finish cutscene
                        self.cut_scene_running = False

        return self.cut_scene_running

    def draw(self, screen):
        #for every lines od dialogue
        for i in range (0, len(self.text)):
            if self.step == i:
                #draw black background, draw narrator box, and text
                if self.step == 0 :
                    pygame.draw.rect(screen, (0,0,0), (0, 0, screen.get_width(), screen.get_height()))
                    pygame.draw.rect(screen, GAME_COLOR['dialogue box'], (0, 550, screen.get_width(), 400))
                    draw_text(screen, self.text[i][0:int(self.text_counter)], 35, GAME_COLOR['text'], 50, 600)

                #draw corresponding background image, draw narrator box, and text
                elif self.step == 5 or self.step == 12:
                    blit_bg_image(screen, 'cutscene3/bg1.png')
                    pygame.draw.rect(screen, GAME_COLOR['dialogue box'], (0, 550, screen.get_width(), 400))
                    draw_text(screen, self.text[i][0:int(self.text_counter)], 35, GAME_COLOR['text'], 50, 600)
                
                else:
                    #draw the corresponding background image, dialogue box, and text
                    blit_bg_image(screen, 'cutscene3/bg1.png')
                    draw_dialog_box(screen)
                    draw_text(screen, self.text[i][0:int(self.text_counter)], 35, GAME_COLOR['text'], 275, 575)

                    #update the chara avatar and expression based on the character speaking at the moment
                    if self.step == 1 or self.step == 2: draw_chara(screen, 'cutscene3/emote1.png')
                    elif self.step == 4: draw_chara(screen, 'cutscene3/emote2.png')
                    elif self.step == 9 or self.step == 10: draw_chara(screen, 'cutscene3/emote3.png')
                    else: draw_chara(screen, 'cutscene3/emote4.png')


class CutSceneFour:
    def __init__(self):
        # Basic setup
        self.name = 'cutscene4' #cutscene's name
        self.step = 0 #on which scene now is the cutscene
        self.cut_scene_running = True #the status of the cutscene

        # Dialogue
        self.setup()
        self.text_counter = 0 #for slide-right text animation

        # Sound when we press LCtrl and go to next step
        self.next_sound = pygame.mixer.Sound('../audio/cutscene.mp3')
        self.next_sound.set_volume(0.3)  

    def setup(self):
        # Append all lines in the story4 in the self.text dictionary
        self.text={}
        file_story4 = open("../story/story4.txt", "r")
        for index, item in enumerate(file_story4.readlines()):
            self.text[index] = item

    def update(self):
         #check if the LCtrl key get pressed or not
        pressed = pygame.key.get_pressed()
        lctrl = pressed[pygame.K_LCTRL]
        
        #for every lines of dialogue
        for i in range(0, len(self.text)):
            #if cutscene is not on the last line of dialogue
            if self.step < len(self.text) - 1:
                #the text animation slide-right effect
                if int(self.text_counter) < len(self.text[i]):
                    self.text_counter += 0.05
                else:
                    #if LCtrl is pressed, go to next scene
                    if lctrl:
                        self.next_sound.play()
                        self.text_counter = 0
                        self.step += 1

            #if cutscene is on the last line of dialogue
            else:
                #text slide-right animation
                if int(self.text_counter) < len(self.text[i]):
                    self.text_counter += 0.05
                else:
                    if lctrl:
                        #finish cutscene
                        self.cut_scene_running = False

        return self.cut_scene_running

    def draw(self, screen):
        #for every lines of dialogue
        for i in range (0, len(self.text)):
            if self.step == i:
                #if it's tthe first line, draw black background
                if self.step == 0 :
                    pygame.draw.rect(screen, (0,0,0), (0, 0, screen.get_width(), screen.get_height()))

                #else, blit background image
                else:
                    blit_bg_image(screen, 'cutscene4/bg1.png')
                    #if it's the 7th or 8th line, blit grandpa's letter image 
                    if self.step == 7 or self.step == 8:
                        letter_grandpa_surf = pygame.image.load('../graphics/dialogue/cutscene4/letter.png')
                        letter_grandpa_rect = letter_grandpa_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 90))
                        screen.blit(letter_grandpa_surf, letter_grandpa_rect)

                #draw narrator box for all of them because there is no dialogue in this cutscene and draw text
                pygame.draw.rect(screen, GAME_COLOR['dialogue box'], (0, 550, screen.get_width(), 400))
                draw_text(screen, self.text[i][0:int(self.text_counter)], 35, GAME_COLOR['text'], 50, 600)


class CutSceneManager:
    def __init__(self, screen):
        #manage cutscene status
        self.cut_scenes_complete = [] #contains name of all completed cutscenes

        #initially there will be no cutscene running
        self.cut_scene = None 
        self.cut_scene_running = False

        #screen to be drawn on
        self.screen = screen

    def start_cut_scene(self, cut_scene):
        #if a cutscene is started, then if it's not completed yet,
        #append the cutscene to the list of completed cutscenes
        if cut_scene.name not in self.cut_scenes_complete: 
            self.cut_scenes_complete.append(cut_scene.name) 

            #set the cutscene to be running            
            self.cut_scene = cut_scene
            self.cut_scene_running = True

    def end_cut_scene(self):
        #the cutscene will stop running
        self.cut_scene = None
        self.cut_scene_running = False

    def update(self):
        #update the cutscene status based on each cutscene
        #if the cutscene reaches the end, then it will be the status will be False
        if self.cut_scene_running:
            self.cut_scene_running = self.cut_scene.update()
        else:
            #if the cut_scene_running becomes False, end the cutscene
            self.end_cut_scene()

    def draw(self):
        #draw the running (active) cutscene
        if self.cut_scene_running:
            self.cut_scene.draw(self.screen)