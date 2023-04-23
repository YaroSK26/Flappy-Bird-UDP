#importovanie kniznic
import pygame
from pygame.locals import *

#zapinanie pygame
pygame.init()

#nastavovanie fps
clock = pygame.time.Clock()
fps = 60

#nastavovanie sirky a dlzky ptm nastavenie na screen + nazov 
screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

#definovanie somarin
ground_scroll = 0
scroll_speed = 4

#nacitavanie obrazkov , musite mat img subor v tom obrazky 
bg = pygame.image.load("img/etika.webp")
ground = pygame.image.load("img/ground.png")

#zapinanie cez terminal - prave tlacitko - run python file in terminal 

#sprite class animacia postavy , images 
class Bird(pygame.sprite.Sprite):
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        #meni obrazky
        self.index =  0 
        #meni rychlost menenia obrazkov
        self.counter = 0
        for num in range(1,4):
            img = pygame.image.load(f"img/bird{num}.png")   
            self.images.append(img)

        self.image = self.images[self.index]
        self.rect  = self.image.get_rect()
        self.rect.center = [x,y]

    def update(self):
        # daco s animacia
        self.counter += 1 
        flap_cooldown = 5

        if self.counter > flap_cooldown:
            self.counter = 0
            self.index += 1 
            if self.index >= len(self.images):
                self.index = 0

        self.image = self.images[self.index]


#nastavenie kde bude flappy zacinat
bird_group = pygame.sprite.Group()
flappy = Bird(100, int(screen_height / 2))
bird_group.add(flappy)



run = True
while run:

    clock.tick(fps)
    
    #nakresli bg
    screen.blit(bg, (0,0))


    bird_group.draw(screen)
    bird_group.update()

    #scrollovanie ground
    screen.blit(ground, (ground_scroll,768))
    ground_scroll -= scroll_speed
    if abs(ground_scroll) > 35:
        ground_scroll = 0
    

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
#cau pygame
pygame.quit()
