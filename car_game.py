#imports
import pygame, sys
from pygame.locals import*
import random, time

#initialize programs
pygame.init()

#FPS assigning
FPS= 60 
clock = pygame.time.Clock()

#colors
blue= (0,0,255)
red = (255,0,0)
green = (0,255,0)
black = (0,0,0)
white = (255,255,255)

#screen set up
screen_width = 400
screen_height = 600
SPEED = 5
score = 0

#setting up fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, black)

background = pygame.image.load('AnimatedStreet.png')

#setting up a white screen
displaysurf = pygame.display.set_mode((screen_width,screen_height))
displaysurf.fill(white)
pygame.display.set_caption("car game")

#enemy class
class enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40,screen_width-40),0)

    def move(self):
        global score
        self.rect.move_ip(0,SPEED)
        if (self.rect.bottom > 600):
            score += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40,screen_width-40),0)

#player class 
class player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160,520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        #if pressed_keys[K_UP]:
            #self.rect.move_ip(0,-5)
        #if pressed_keys[K_DOWN]:
            #self.rect.move_ip(-5,0)
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip (-5,0)
        if self.rect.right < screen_width:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5,0)


#player and enemy 
P1= player()
E1= enemy()

#creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

#adding a new user event
inc_speed = pygame.USEREVENT +1
pygame.time.set_timer(inc_speed,1000)

#game loop
while True:

    #quit the game correctly
    for event in pygame.event.get():
        if event.type == inc_speed:
            SPEED +=0.5

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    #update the sprite and time
    displaysurf.blit(background,(0,0))
    scores = font_small.render(str(score),True, black)
    displaysurf.blit(scores, (10,10))

    #moves and re_draws all sprites
    for entity in all_sprites:
        displaysurf.blit(entity.image,entity.rect)
        entity.move()

    #collision
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(0.5)

        displaysurf.fill(red)
        displaysurf.blit(game_over,(30,250))

        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()


    pygame.display.update()
    clock.tick(FPS)
