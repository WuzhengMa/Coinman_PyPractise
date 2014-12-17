# -*- coding: utf-8 -*-
#A code by Wuzheng Ma

import sys, pygame, random
from pygame.locals import *
from sys import exit
BACKGROUND = 'QQ空间背景专用.jpg'


pygame.init()

#Initialize the screen
caption = pygame.display.set_caption('Gettingcoins')
screen = pygame.display.set_mode((480,640),0,32)
background = pygame.image.load(BACKGROUND).convert()

#class Soldier
class Soldier(pygame.sprite.Sprite):
    def __init__(self, soldier_position=[0,0], Sspeed=[0,0]):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('image3.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = soldier_position  
        self.speed = Sspeed
    def run(self):
        self.rect = self.rect.move(self.speed)  

#class weapon
class Weapon_drop(pygame.sprite.Sprite):
    def __init__(self, weapon_position=[0,0], Wspeed=[0,0]):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('image57.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = weapon_position
        self.speed = Wspeed
    def move(self):
        self.rect = self.rect.move(self.speed)    

game_level = 1             
LorR = 0 #The one to control which side the soldier will go,left or right
aSoldier = Soldier([240, 500], [LorR, 0])     
count_drop = 0 # Counter for the dropping weapon
flag_hold = False
flag_edge = True                                                                                                                           
weaponx = random.randint(20, 460)   
aWeapon = Weapon_drop([weaponx, 100], [0, 1])
font1 = pygame.font.Font(None, 36)
font2 = pygame.font.Font(None, 40)
font3 = pygame.font.Font(None, 80)
text = font1.render("+10", True, (255,0,0))
count_score = 0 #Counter for the total score
text_score_total = font2.render("Total Score: %d" % count_score,\
True, (255,0,0))
flag_text = False 
count_text = 0 #Counter for the score added each time collision happens
flag_levelup = False
game_fail = False
gameover = font3.render("Game Over !", True, (255,0,0))

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
         #Use the keyboard to control the soldier
        if event.type == KEYDOWN:   
            if event.key == K_LEFT:  #left buttom
                LorR = -1
                aSoldier = Soldier([aSoldier.rect[0], 500], [LorR, 0])
                aSoldier.run()    
                flag_hold = True
            elif event.key == K_RIGHT:   #Right buttom
                LorR = 1
                aSoldier = Soldier([aSoldier.rect[0], 500], [LorR, 0])
                aSoldier.run()
                flag_hold = True       
        elif event.type == KEYUP:
            flag_hold = False        
    if flag_hold == True and flag_edge == True:   #Hold the buttom, keep the soldier moving 
        aSoldier.run()
        #In case of the soldier is running out of range
        
        #Case 1, let the soldier running out from one end
        if aSoldier.rect[0] < 0:
            aSoldier.rect[0] = 480
            aSoldier = Soldier([aSoldier.rect[0], 500], [LorR, 0])
            aSoldier.run()
        #Case 2 
        elif aSoldier.rect[0] > 480:
            aSoldier.rect[0] = 0
            aSoldier = Soldier([aSoldier.rect[0], 500], [LorR, 0])
            aSoldier.run()  

      
                  
    #Control the dropping speed of the weapon   
    if count_drop%10==0:
        aWeapon.move()
    #Dont catch the weapon will fail the game
    if aWeapon.rect[1] > 650:   
            game_fail = True 

    #If collide, draw a new sprite randomly
    if pygame.sprite.collide_rect(aSoldier, aWeapon) and aWeapon.rect[1] < 500:
        
        #Record where they collide
        where_collide = [aWeapon.rect[0], aWeapon.rect[1]]
        
        #Update the weapon position right after collision
        weaponx = random.randint(50, 400)
        aWeapon = Weapon_drop([weaponx, 100],[0,game_level])
        count_drop = 0
                       
        flag_text = True # Output '+5'
        flag_levelup = True  #Ready to level-up 
        count_score+=10
        #Update the total score
        text_score_total = font2.render("Total Score: %d" % count_score,\
        True, (255,0,0))

    
    #Use the score to control the game level        
    if count_score%50 == 0 and count_score != 0 and flag_levelup == True:
        game_level+=1
        flag_levelup = False
        print game_level    
        
    #Control to output the text "+5"
    if flag_text==True:
        count_text+=1
        if count_text > 1000:
            flag_text = False
            count_text = 0
                      
    #draw the change for each time in the loop        
    screen.blit(background, [0,0])  
    screen.blit(aWeapon.image, aWeapon.rect)
    screen.blit(aSoldier.image, aSoldier.rect)      
    screen.blit(text_score_total,[50,50])
    if count_text < 1000 and flag_text == True:
        screen.blit(text,[where_collide[0], where_collide[1]]) 
    if game_fail == True:
        screen.fill([255,255,255]) 
        screen.blit(gameover, [80,250])  
    pygame.display.update()
    
    count_drop+=1
            
          
