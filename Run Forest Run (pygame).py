#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pygame
from sys import exit
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1=pygame.image.load('Jueguito/Player/player_walk_1.png').convert_alpha()
        player_walk_2=pygame.image.load('Jueguito/Player/player_walk_2.png').convert_alpha()
        self.player_walk= [player_walk_1,player_walk_2]
        self.player_index = 0
        self.player_jump=pygame.image.load('Jueguito/Player/jump.png').convert_alpha()

        self.image =self.player_walk[self.player_index]
        self.rect  = self.image.get_rect(midbottom =(80,300))
        self.gravity=0
        self.jump_sound= pygame.mixer.Sound('Jueguito/Salto.ogg')
    
    def player_input(self):
        keys =pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom>=300:
            self.gravity=-20
            self.jump_sound.play()
    
    def apply_gravity(self):
        self.gravity+=1
        self.rect.y+=self.gravity
        if self.rect.bottom>=300:
            self.rect.bottom=300
    
    
    def animation_state(self):
        if self.rect.bottom <300:
            self.image=self.player_jump
        else:
            self.player_index +=0.1
            if self.player_index >=len(self.player_walk):
                self.player_index= 0
                self.image=self.player_walk[int(self.player_index)]
        
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
            
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if type =="fly":
            fly_1=pygame.image.load('Jueguito/Fly/flyFly1.png').convert_alpha()
            fly_2=pygame.image.load('Jueguito/Fly/flyFly2.png').convert_alpha()
            self.frames=[fly_1,fly_2]
            y_pos =210
        else:
            snail_1=pygame.image.load('Jueguito/Snail/snail1.png').convert_alpha()
            snail_2=pygame.image.load('Jueguito/Snail/snail2.png').convert_alpha()
            self.frames =[snail_1,snail_2]
            y_pos=300
            
        self.animation_index=0
        self.image=self.frames[self.animation_index]
        self.rect =self.image.get_rect(midbottom=(randint(900,1100),y_pos))

    def animation_state(self):
        self.animation_index+=0.1
        if self.animation_index>=len(self.frames):
            self.animation_index=0
            self.image=self.frames[int(self.animation_index)]
            
    def update(self):
        self.animation_state()
        self.rect.x -=6
        self.destroy()
    
    def destroy(self):
        if self.rect.x<=-100:
            self.kill()
        

def display_score():
        current_time =round((pygame.time.get_ticks()-start_time)/1000,2)
        score_surf=test_font.render(f'{current_time}',False,(64,64,64))
        score_rect=score_surf.get_rect(center =(400,50))
        screen.blit(score_surf,score_rect)
        return current_time
    
def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom==300:
                screen.blit(snail_surface,obstacle_rect)
            else:
                screen.blit(fly_surf,obstacle_rect)
            
        obstacle_list= [obstacle for obstacle in obstacle_list if obstacle_rect.x > -100]
        return obstacle_list
    else: return []       

def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else:
        return True
    
def player_animation():
    global player_surface, player_index
    if player_rect.bottom < 300:
        player_surface=player_jump
    else:
        player_index+=0.1
        if player_index>= len(player_walk):
            player_index=0
        player_surface=player_walk[int(player_index)]
       




pygame.init() #Prendido
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Run Forest Run")
clock =pygame.time.Clock() 
game_active =True
start_time=0
final_score=0

bg_Music =pygame.mixer.Sound('Jueguito/music.wav')
bg_Music.play(loops=-1)
bg_Music.set_volume(0.2)
player= pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group=pygame.sprite.Group()


#Segunda forma. Imagen
sky_surface=pygame.image.load('Jueguito/Imagenes/Sky.png').convert()
ground_surface=pygame.image.load('Jueguito/Imagenes/ground.png').convert()

#Tercera forma. Suface with text

test_font=pygame.font.Font('Jueguito/Font/Pixeltype.ttf',50)
text_surface =test_font.render('Run Forest Run',False,"Black").convert() 

play_again_surf=test_font.render('Press Space to play again', False, "Black")
play_again_rect=play_again_surf.get_rect(center=(400,50))


#Carga de jugadores y obstaculos

#Obstacles y enemies
snail_frame_1=pygame.image.load('Jueguito/Snail/snail1.png').convert_alpha()
snail_frame_2=pygame.image.load('Jueguito/Snail/snail2.png').convert_alpha()
snail_x_pos= 600
snail_frames = [snail_frame_1,snail_frame_2]
snail_frame_index=0
snail_surface =snail_frames[snail_frame_index]
snail_rect=snail_surface.get_rect(bottomright=(snail_x_pos,300))

fly_frame_1=pygame.image.load('Jueguito/Fly/flyFly1.png').convert_alpha()
fly_frame_2=pygame.image.load('Jueguito/Fly/flyFly2.png').convert_alpha()
fly_frames =[fly_frame_1,fly_frame_2]
fly_frame_index=0
fly_surf=fly_frames[fly_frame_index]


obstacle_rect_list=[]

#Player
player_walk_1=pygame.image.load('Jueguito/Player/player_walk_1.png').convert_alpha()
player_walk_2=pygame.image.load('Jueguito/Player/player_walk_2.png').convert_alpha()
player_walk= [player_walk_1,player_walk_2]
player_index = 0
player_jump=pygame.image.load('Jueguito/Player/jump.png').convert_alpha()

player_surface =player_walk[player_index]

player_rect=player_surface.get_rect(midbottom=(80,300))
player_gravity = 0
player_stand= pygame.image.load('Jueguito/Player/player_stand.png').convert_alpha()
#player_stand=pygame.transform.scale(player_stand,(200,400))
player_stand_rect=player_stand.get_rect(center =(400,200))


#Titulo
title=test_font.render("You died", False,"Black")
title_rect =title.get_rect(center=(400,300))


###Timer

obstacle_timer =pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

snail_animation_timer=pygame.USEREVENT+2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer=pygame.USEREVENT+3
pygame.time.set_timer(fly_animation_timer,200)


#Main loop

while True:
    for event in pygame.event.get(): 
        if event.type== pygame.QUIT: 
            pygame.quit()
            exit()
        if game_active:    
            if event.type==pygame.MOUSEBUTTONDOWN: 
                if player_rect.collidepoint(event.pos) and player_rect.bottom>=300 : 
                    player_gravity=-20
            if event.type== pygame.KEYDOWN and player_rect.bottom >=300:
                if event.key==pygame.K_SPACE:
                    player_gravity =-20
        else:
            if event.type ==pygame.KEYDOWN and event.key==pygame.K_SPACE:
                game_active=True
                snail_rect.left=800
                start_time=pygame.time.get_ticks()
        
        if game_active:
            if event.type==obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))

            if event.type==snail_animation_timer:
                if snail_frame_index==0:
                    snail_frame_index=1
                else: 
                    snail_frame_index=0
                snail_surface=snail_frames[snail_frame_index]
                
            if event.type==fly_animation_timer:
                if fly_frame_index==0:
                    fly_frame_index=1
                else: 
                    fly_frame_index=0
                fly_surf=fly_frames[fly_frame_index]
    
      
    ###########################################################
    #Superposición de surfaces
    if game_active:   
        screen.blit(sky_surface,(0,0)) 
        screen.blit(ground_surface,(0,300))
        final_score = display_score()
        player.draw(screen)
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()  
        game_active=collision_sprite()
        
    ###Death Screen        
    else:
        screen.fill((94,129,168))
        screen.blit(play_again_surf,play_again_rect)
        screen.blit(player_stand, player_stand_rect)
        screen.blit(title, title_rect)
        player_gravity=0
        score_mess=test_font.render(f'Your Score is: {final_score}',False,"Black")
        score_mess_rect=score_mess.get_rect(center=(400,350))
        screen.blit(score_mess,score_mess_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom=(80,300)

    pygame.display.update()
    clock.tick(60) 




# In[ ]:




