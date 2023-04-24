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
screen_height = 836

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

#definovanie somarin
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False

#nacitavanie obrazkov , musite mat img subor v tom obrazky 
bg = pygame.image.load("img/etika.webp")
ground_img = pygame.image.load("img/ground.png")

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
        self.vel = 0
        self.clicked = False

    def update(self):
        #nastavovanie gravity
        if flying == True:
            self.vel += 0.5
            if self.vel >8:
                self.vel = 8
            print(self.vel)
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)



        if game_over == False:
            #jumping
            if pygame.mouse.get_pressed()[0]==1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            #nastavovanie aby pri drzani mysi fľepi neskakal
            if pygame.mouse.get_pressed()[0]==0:
                self.clicked = False

            # cooldown na obrazky -animacia
            self.counter += 1 
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1 
                if self.index >= len(self.images):
                    self.index = 0

            self.image = self.images[self.index]



                #rotating bird po skakani , 
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -1)
        else:
             self.image = pygame.transform.rotate(self.images[self.index],-90)









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

    #nakresli ground
    screen.blit(ground_img, (ground_scroll , 768))

    #ked fľepi hitne ground
    if flappy.rect.bottom > 768:
        game_over = True
        flying = False

    if game_over == False:

    #scrollovanie ground
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0
    

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    pygame.display.update()
#cau pygame
pygame.quit()
