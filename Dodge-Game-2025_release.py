import pygame
from random import randrange,choice,random

player_speed=30
bad_guy_speed=5
bad_guy_delay=20
max_bad_guys=1
bad_guys_to_level_up=5


#GAME WINDOW

pygame.init()
clock = pygame.time.Clock()
SCREEN_WIDTH = 800
SCREEN_HEIGHT=int(SCREEN_WIDTH*0.8)
screen=pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #create window
screen_rect = screen.get_rect()

player=pygame.Rect(300,250, 50, 50)

class level():
    def __init__(self,bad_guy_speed,bad_guy_delay,max_bad_guys):
        self.level=1
        self.max_bad_guys=max_bad_guys
        self.bad_guy_delay=bad_guy_delay
        self.bad_guys_in_level=max_bad_guys
        self.bad_guy_speed = bad_guy_speed
    
    def level_up(self):
        self.level=self.level+1
        self.bad_guy_delay=self.bad_guy_delay/1.5
        self.max_bad_guys=self.max_bad_guys+1
        self.bad_guy_speed=self.bad_guy_speed+bad_guy_speed*0.25
        self.bad_guys_in_level=0
        
def move_player():
    key=pygame.key.get_pressed()
    if key[pygame.K_a]:
        player.move_ip(-player_speed,0)
    elif key[pygame.K_d]:
        player.move_ip(player_speed,0)
    elif key[pygame.K_w]:
        player.move_ip(0,-player_speed)
    elif key[pygame.K_s]:
        player.move_ip(0,player_speed)      
    player.clamp_ip(screen_rect)

def spawn_baddie(bad_guys,level):
    possible_sides = ['top','bottom','left','right']
    if len(bad_guys) < level.max_bad_guys:
        mychoice=choice(possible_sides)
        if mychoice=='top':
            bad_guys.append([pygame.Rect(randrange(0,SCREEN_WIDTH),0, 50,50),0,mychoice])
        elif mychoice=='bottom':
            bad_guys.append([pygame.Rect(randrange(0,SCREEN_WIDTH),SCREEN_HEIGHT-50, 50,50),0,mychoice])
        elif mychoice=='left':
            bad_guys.append([pygame.Rect(0,randrange(50,SCREEN_HEIGHT-50), 50,50),0,mychoice])
        elif mychoice=='right':
            bad_guys.append([pygame.Rect(SCREEN_WIDTH-50,randrange(50,SCREEN_HEIGHT-50), 50,50),0,mychoice])
            
def move_baddie(bad_guy,level):
    if bad_guy[1]>level.bad_guy_delay:
        if bad_guy[2]=='top':
            bad_guy[0].move_ip(0,level.bad_guy_speed) 
        if bad_guy[2]=='bottom':
            bad_guy[0].move_ip(0,-level.bad_guy_speed)
        if bad_guy[2]=='left':
            bad_guy[0].move_ip(level.bad_guy_speed,0)
        elif bad_guy[2]=='right':
            bad_guy[0].move_ip(-level.bad_guy_speed,0)
        
def check_close(run):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
    return run
    
def main(run):
    curr_level=level(bad_guy_speed,bad_guy_delay,max_bad_guys)
    bad_guys=[]
    while run:
        screen.fill((0,0,0))
        
        if curr_level.bad_guys_in_level > bad_guys_to_level_up*curr_level.max_bad_guys:
            curr_level.level_up()
            print("level {}".format(curr_level.level))
        #bad guys turn
        spawn_baddie(bad_guys,curr_level)
        for x in range(len(bad_guys)):
            pygame.draw.rect(screen,(0,255,0),bad_guys[x][0])
            bad_guys[x][1]=bad_guys[x][1]+1
            move_baddie(bad_guys[x],curr_level)                               
            if bad_guys[x][0].colliderect(player):
                run=False
            if bad_guys[x][0].left < 0 or bad_guys[x][0].right > SCREEN_WIDTH or bad_guys[x][0].top < 0 or bad_guys[x][0].bottom > SCREEN_HEIGHT:
                del bad_guys[x]
                curr_level.bad_guys_in_level=curr_level.bad_guys_in_level+1
                break
                
        #player's turn
        pygame.draw.rect(screen,(255,0,0), player)
        move_player()
           

        #event handler
        run=check_close(run)
        pygame.display.update()
        clock.tick(60)
    
if __name__ == '__main__':
    main(True)
    pygame.quit()