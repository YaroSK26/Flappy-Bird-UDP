#importovanie kniznic
import pygame
from pygame.locals import *
import random

#pajgejm
pygame.init()

#fps
clock = pygame.time.Clock()
fps = 300

#rozmery obrazovky
screen_width = 864
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

#definovanie fontu
font = pygame.font.SysFont("comic sans MS", 60)
menu_font = pygame.font.SysFont('gabriola', 140)


#definovanie farieb
white = (255, 255, 255)
#definovanie premennych
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 200
pipe_frequency = 2000  # milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False

#nacitavanie obrazkov
bg = pygame.image.load("img/etika.webp")
ground_img = pygame.image.load("img/ground.png")
reset_button_img = pygame.image.load("img/chleba.png")
menu_img = pygame.image.load("img/menu.png")
endless_button = pygame.image.load('img/endless1.png')
quit_button = pygame.image.load("img/Quit1.png")
levels_button = pygame.image.load("img/level1.png")
level1 = pygame.image.load('img/lvl1arab.png')
level2 = pygame.image.load('img/lvl2arab.png')
level3 = pygame.image.load('img/lvl3arab.png')
level4 = pygame.image.load('img/lvl4arab.png')
level5 = pygame.image.load('img/lvl5arab.png')
anglictina = pygame.image.load('img/gb.png')
quit_hu = pygame.image.load('img/quit_hu.png')
reset_hu = pygame.image.load('img/reset_hu.png')
endless_hu = pygame.image.load('img/endless_hu.png')
levels_hu = pygame.image.load('img/levels_hu.png')
madarcina = pygame.image.load('img/hu2.png')

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
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)



        if game_over == False:
            #jumping
            if pygame.mouse.get_pressed()[0]==1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            #nastavovanie aby pri drzani mysi fÄ¾epi neskakal
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

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.disabled = False
    def draw(self):
        
        action = False

        #pozicia kurozra
        pos = pygame.mouse.get_pos()
        if not self.disabled:
            #ci je mys nad chlebom
            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1:
                    action = True

        else:
            # Render the disabled appearance of the button
            self.image.set_alpha(256)  # Adjust the transparency to indicate disabled state
            return False  # Return False when the button is disabled
        
        #chleba
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

#nastavenie kde bude flappy zacinat a kde budu pipy
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()
flappy = Bird(100, int(screen_height / 2))
bird_group.add(flappy)

#chleba instancia
button = Button(screen_width // 2.33, screen_height // 2.3, reset_button_img)
menu_button = Button(screen_width // 2.33, screen_height // 1.9, menu_img)


def hra_po_madarsky():
    pygame.display.set_caption('Menu')
    while True:

        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    endless_button_x = screen_width // 2 - endless_button.get_width() // 2
                    endless_button_y = screen_height // 2 - endless_button.get_height() // 2
                    endless_button_rect = endless_button.get_rect(topleft=(endless_button_x, endless_button_y))

                    if endless_button_rect.collidepoint(mouse_x, mouse_y):
                        game_over = False
                        endless_level()
                        
                        

                    quit_button_x = screen_width // 2 - quit_button.get_width() // 2
                    quit_button_y = screen_height // 1.4 - quit_button.get_height() // 2
                    quit_button_rect = quit_button.get_rect(topleft=(quit_button_x, quit_button_y))

                    if quit_button_rect.collidepoint(mouse_x, mouse_y):
                        pygame.quit()
                        exit()

                    levels_button_x = screen_width // 2 - levels_button.get_width() // 2
                    levels_button_y = screen_height // 1.65 - levels_button.get_height() // 2
                    levels_button_rect = levels_button.get_rect(topleft=(levels_button_x, levels_button_y))

                    if levels_button_rect.collidepoint(mouse_x, mouse_y):
                        levels_menu()
                      
                    anglictina_x = screen_width // 2.6 - anglictina.get_width() // 2
                    anglictina_y = screen_height // 1.1 - anglictina.get_height() // 2
                    anglictina_button_rect = anglictina.get_rect(topleft=(anglictina_x, anglictina_y))

                    if anglictina_button_rect.collidepoint(mouse_x,mouse_y):
                        hra_po_anglicky()

                    madarcina_x = screen_width // 1.6 - madarcina.get_width() // 2
                    madarcina_y = screen_height // 1.1 - madarcina.get_height() // 2
                    madarcina_button_rect = madarcina.get_rect(topleft=(madarcina_x, madarcina_y))

                    if madarcina_button_rect.collidepoint(mouse_x, mouse_y):
                        hra_po_madarsky()


        screen.blit(bg, (0, 0))

        MENU_TEXT = menu_font.render('Madar Csakpodo', True, '#111111')
        screen.blit(MENU_TEXT, (screen_width // 2 - MENU_TEXT.get_width() // 2, screen_height // 6 - MENU_TEXT.get_height() // 2))
        endless_hu_x = screen_width // 2 - endless_hu.get_width() // 2
        endless_hu_y = screen_height // 2 - endless_hu.get_height() // 2
        screen.blit(endless_hu, (endless_hu_x, endless_hu_y))

        quit_hu_x = screen_width // 2 - quit_hu.get_width() // 2
        quit_hu_y = screen_height // 1.4 - quit_hu.get_height() // 2
        screen.blit(quit_hu, (quit_hu_x, quit_hu_y))

        levels_hu_x = screen_width // 2 - levels_hu.get_width() // 2
        levels_hu_y = screen_height // 1.65 - levels_hu.get_height() // 2
        screen.blit(levels_hu, (levels_hu_x, levels_hu_y))

        anglictina_x = screen_width // 2.6 - anglictina.get_width() // 2
        anglictina_y = screen_height // 1.1 - anglictina.get_height() // 2
        screen.blit(anglictina, (anglictina_x, anglictina_y))

        madarcina_x = screen_width // 1.6 - madarcina.get_width() // 2
        madarcina_y = screen_height // 1.1 - madarcina.get_height() // 2
        screen.blit(madarcina, (madarcina_x, madarcina_y))
        pygame.display.update()
        clock.tick(fps)

def hra_po_anglicky():
    pygame.display.set_caption('Menu')
    while True:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    endless_button_x = screen_width // 2 - endless_button.get_width() // 2
                    endless_button_y = screen_height // 2 - endless_button.get_height() // 2
                    endless_button_rect = endless_button.get_rect(topleft=(endless_button_x, endless_button_y))

                    if endless_button_rect.collidepoint(mouse_x, mouse_y):
                        game_over = False
                        endless_level()
                        

                    quit_button_x = screen_width // 2 - quit_button.get_width() // 2
                    quit_button_y = screen_height // 1.4 - quit_button.get_height() // 2
                    quit_button_rect = quit_button.get_rect(topleft=(quit_button_x, quit_button_y))

                    if quit_button_rect.collidepoint(mouse_x, mouse_y):
                        pygame.quit()
                        exit()

                    levels_button_x = screen_width // 2 - levels_button.get_width() // 2
                    levels_button_y = screen_height // 1.65 - levels_button.get_height() // 2
                    levels_button_rect = levels_button.get_rect(topleft=(levels_button_x, levels_button_y))

                    if levels_button_rect.collidepoint(mouse_x, mouse_y):
                        levels_menu()
                      
                    anglictina_x = screen_width // 2.6 - anglictina.get_width() // 2
                    anglictina_y = screen_height // 1.1 - anglictina.get_height() // 2
                    anglictina_button_rect = anglictina.get_rect(topleft=(anglictina_x, anglictina_y))

                    if anglictina_button_rect.collidepoint(mouse_x,mouse_y):
                        hra_po_anglicky()

                    madarcina_x = screen_width // 1.6 - madarcina.get_width() // 2
                    madarcina_y = screen_height // 1.1 - madarcina.get_height() // 2
                    madarcina_button_rect = madarcina.get_rect(topleft=(madarcina_x, madarcina_y))

                    if madarcina_button_rect.collidepoint(mouse_x, mouse_y):
                        hra_po_madarsky()


        screen.blit(bg, (0, 0))

        MENU_TEXT = menu_font.render('Flappy Bird', True, '#111111')
        screen.blit(MENU_TEXT, (screen_width // 2 - MENU_TEXT.get_width() // 2, screen_height // 6 - MENU_TEXT.get_height() // 2))
        endless_button_x = screen_width // 2 - endless_button.get_width() // 2
        endless_button_y = screen_height // 2 - endless_button.get_height() // 2
        screen.blit(endless_button, (endless_button_x, endless_button_y))

        quit_button_x = screen_width // 2 - quit_button.get_width() // 2
        quit_button_y = screen_height // 1.4 - quit_button.get_height() // 2
        screen.blit(quit_button, (quit_button_x, quit_button_y))

        levels_button_x = screen_width // 2 - levels_button.get_width() // 2
        levels_button_y = screen_height // 1.65 - levels_button.get_height() // 2
        screen.blit(levels_button, (levels_button_x, levels_button_y))

        anglictina_x = screen_width // 2.6 - anglictina.get_width() // 2
        anglictina_y = screen_height // 1.1 - anglictina.get_height() // 2
        screen.blit(anglictina, (anglictina_x, anglictina_y))

        madarcina_x = screen_width // 1.6 - madarcina.get_width() // 2
        madarcina_y = screen_height // 1.1 - madarcina.get_height() // 2
        screen.blit(madarcina, (madarcina_x, madarcina_y))
        pygame.display.update()
        clock.tick(fps)


        screen.blit(bg, (0, 0))

        MENU_TEXT = menu_font.render('Flappy Bird', True, '#111111')
        screen.blit(MENU_TEXT, (screen_width // 2 - MENU_TEXT.get_width() // 2, screen_height // 6 - MENU_TEXT.get_height() // 2))
        endless_button_x = screen_width // 2 - endless_button.get_width() // 2
        endless_button_y = screen_height // 2 - endless_button.get_height() // 2
        screen.blit(endless_button, (endless_button_x, endless_button_y))

        quit_button_x = screen_width // 2 - quit_button.get_width() // 2
        quit_button_y = screen_height // 1.4 - quit_button.get_height() // 2
        screen.blit(quit_button, (quit_button_x, quit_button_y))

        levels_button_x = screen_width // 2 - levels_button.get_width() // 2
        levels_button_y = screen_height // 1.65 - levels_button.get_height() // 2
        screen.blit(levels_button, (levels_button_x, levels_button_y))

        anglictina_x = screen_width // 2.6 - anglictina.get_width() // 2
        anglictina_y = screen_height // 1.1 - anglictina.get_height() // 2
        screen.blit(anglictina, (anglictina_x, anglictina_y))

        madarcina_x = screen_width // 1.6 - madarcina.get_width() // 2
        madarcina_y = screen_height // 1.1 - madarcina.get_height() // 2
        screen.blit(madarcina, (madarcina_x, madarcina_y))
        pygame.display.update()
        clock.tick(fps)
    

#definovanie pipy
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/etika.png')
        self.rect = self.image.get_rect()
        
        # pozicia 1 je z vrchu, -1  z dola
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]
        
    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()
        

#chleba


def start_game():
    screen.blit(bg, (0, 0))
    global flying, game_over, score
    flying = True
    game_over = False
    score = reset_game()

    pygame.display.set_caption('Menu')

def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    score = 0
    return score
    




def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
    button.disabled = False
    






def start_level1():
    button.disabled = False
    global flying, game_over, score, ground_scroll, last_pipe, pass_pipe
    flying = True
    game_over = False
    score = reset_game()
    pipe_frequency = 2400
    pipe_gap = 170


    screen.fill((0, 0, 0))
    napisfont = pygame.font.SysFont('mvboli', 140)
    text = napisfont.render("Etika", True, (255, 255, 0))
    text_rect = text.get_rect(center=(screen_width // 2.05, screen_height // 2))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.delay(2000)

    while True:
        clock.tick(fps)
        screen.blit(bg, (0, 0))
        bird_group.draw(screen)
        bird_group.update()
        pipe_group.draw(screen)
        screen.blit(ground_img, (ground_scroll, 768))

        if len(pipe_group) > 0:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
                    and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right \
                    and pass_pipe == False:
                pass_pipe = True
            if pass_pipe == True:
                if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                    score += 1
                    pass_pipe = False

        draw_text(str(score), font, white, int(screen_width / 2.1), 20)
        if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
            game_over = True
        if flappy.rect.bottom >= 768:
            game_over = True
            flying = False

        if game_over == False and flying == True:
            time_now = pygame.time.get_ticks()
            if time_now - last_pipe > pipe_frequency:
                pipe_height = random.randint(-pipe_gap // 2, pipe_gap // 2)
                btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height + pipe_gap // 2, -1)
                top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height - pipe_gap // 2, 1)
                pipe_group.add(btm_pipe)
                pipe_group.add(top_pipe)
                last_pipe = time_now
            ground_scroll -= scroll_speed
            if abs(ground_scroll) > 35:
                ground_scroll = 0
            pipe_group.update()

        if game_over == True:
            if menu_button.draw() == True:
                button.disabled = True
                main_menu()
            if button.draw() == True:
                start_level1()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
                flying = True

        pygame.display.update()

def start_level2():
    button.disabled = False
    global flying, game_over, score, ground_scroll, last_pipe, pass_pipe
    flying = True
    game_over = False
    score = reset_game()
    pipe_frequency = 1700
    pipe_gap = 100

    screen.fill((0, 0, 0))  
    napisfont = pygame.font.SysFont('mvboli', 140)
    text = napisfont.render("Slovencina", True, (150, 75, 0))
    text_rect = text.get_rect(center=(screen_width // 2.05, screen_height // 2))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.delay(2000)  


    while True:
        clock.tick(fps)
        screen.blit(bg, (0, 0))
        bird_group.draw(screen)
        bird_group.update()
        pipe_group.draw(screen)
        screen.blit(ground_img, (ground_scroll, 768))

        if len(pipe_group) > 0:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
                    and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right \
                    and pass_pipe == False:
                pass_pipe = True
            if pass_pipe == True:
                if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                    score += 1
                    pass_pipe = False

        draw_text(str(score), font, white, int(screen_width / 2.1), 20)
        if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
            game_over = True
        if flappy.rect.bottom >= 768:
            game_over = True
            flying = False

        if game_over == False and flying == True:
            time_now = pygame.time.get_ticks()
            if time_now - last_pipe > pipe_frequency:
                pipe_height = random.randint(-pipe_gap // 2, pipe_gap // 2)
                btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height + pipe_gap // 2, -1)
                top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height - pipe_gap // 2, 1)
                pipe_group.add(btm_pipe)
                pipe_group.add(top_pipe)
                last_pipe = time_now
            ground_scroll -= scroll_speed
            if abs(ground_scroll) > 35:
                ground_scroll = 0
            pipe_group.update()

        if game_over == True:
            if menu_button.draw() == True:
                button.disabled = True
                main_menu()
            if button.draw() == True:
                start_level2()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
                flying = True

        pygame.display.update()

def start_level3():
    button.disabled = False
    global flying, game_over, score, ground_scroll, last_pipe, pass_pipe
    flying = True
    game_over = False
    score = reset_game()
    pipe_frequency = 1400
    pipe_gap = 80

    screen.fill((0, 0, 0))  
    napisfont = pygame.font.SysFont('mvboli', 140)
    text = napisfont.render("Matematika", True, (0, 255, 0))
    text_rect = text.get_rect(center=(screen_width // 2.05, screen_height // 2))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.delay(2000)  


    while True:
        clock.tick(fps)
        screen.blit(bg, (0, 0))
        bird_group.draw(screen)
        bird_group.update()
        pipe_group.draw(screen)
        screen.blit(ground_img, (ground_scroll, 768))

        if len(pipe_group) > 0:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
                    and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right \
                    and pass_pipe == False:
                pass_pipe = True
            if pass_pipe == True:
                if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                    score += 1
                    pass_pipe = False

        draw_text(str(score), font, white, int(screen_width / 2.1), 20)
        if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
            game_over = True
        if flappy.rect.bottom >= 768:
            game_over = True
            flying = False

        if game_over == False and flying == True:
            time_now = pygame.time.get_ticks()
            if time_now - last_pipe > pipe_frequency:
                pipe_height = random.randint(-pipe_gap // 2, pipe_gap // 2)
                btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height + pipe_gap // 2, -1)
                top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height - pipe_gap // 2, 1)
                pipe_group.add(btm_pipe)
                pipe_group.add(top_pipe)
                last_pipe = time_now
            ground_scroll -= scroll_speed
            if abs(ground_scroll) > 35:
                ground_scroll = 0
            pipe_group.update()

        if game_over == True:
            if menu_button.draw() == True:
                button.disabled = True
                main_menu()
            if button.draw() == True:
                start_level3()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
                flying = True

        pygame.display.update()

def start_level4():
    button.disabled = False
    global flying, game_over, score, ground_scroll, last_pipe, pass_pipe
    flying = True
    game_over = False
    score = reset_game()
    pipe_frequency = 1050
    pipe_gap = 45

    screen.fill((0, 0, 0))  
    napisfont = pygame.font.SysFont('mvboli', 100)
    text = napisfont.render("Elektrotechnika", True, (0, 0, 255))
    text_rect = text.get_rect(center=(screen_width // 2.05, screen_height // 2))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.delay(2000)  


    while True:
        clock.tick(fps)
        screen.blit(bg, (0, 0))
        bird_group.draw(screen)
        bird_group.update()
        pipe_group.draw(screen)
        screen.blit(ground_img, (ground_scroll, 768))

        if len(pipe_group) > 0:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
                    and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right \
                    and pass_pipe == False:
                pass_pipe = True
            if pass_pipe == True:
                if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                    score += 1
                    pass_pipe = False

        draw_text(str(score), font, white, int(screen_width / 2.1), 20)
        if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
            game_over = True
        if flappy.rect.bottom >= 768:
            game_over = True
            flying = False

        if game_over == False and flying == True:
            time_now = pygame.time.get_ticks()
            if time_now - last_pipe > pipe_frequency:
                pipe_height = random.randint(-pipe_gap // 2, pipe_gap // 2)
                btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height + pipe_gap // 2, -1)
                top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height - pipe_gap // 2, 1)
                pipe_group.add(btm_pipe)
                pipe_group.add(top_pipe)
                last_pipe = time_now
            ground_scroll -= scroll_speed
            if abs(ground_scroll) > 35:
                ground_scroll = 0
            pipe_group.update()

        if game_over == True:
            if menu_button.draw() == True:
  
                main_menu()
            if button.draw() == True:
                button.disabled = True
                start_level4()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
                flying = True

        pygame.display.update()

def start_level5():
    button.disabled = False
    global flying, game_over, score, ground_scroll, last_pipe, pass_pipe
    flying = True
    game_over = False
    score = reset_game()
    pipe_frequency = 710
    pipe_gap = 20

    screen.fill((0, 0, 0))  
    napisfont = pygame.font.SysFont('mvboli', 80)
    text = napisfont.render("Hardware pocitaca", True, (255, 0, 0))
    text_rect = text.get_rect(center=(screen_width // 2.05, screen_height // 2))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.delay(2000)  


    while True:
        clock.tick(fps)
        screen.blit(bg, (0, 0))
        bird_group.draw(screen)
        bird_group.update()
        pipe_group.draw(screen)
        screen.blit(ground_img, (ground_scroll, 768))

        if len(pipe_group) > 0:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
                    and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right \
                    and pass_pipe == False:
                pass_pipe = True
            if pass_pipe == True:
                if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                    score += 1
                    pass_pipe = False

        draw_text(str(score), font, white, int(screen_width / 2.1), 20)
        if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
            game_over = True
        if flappy.rect.bottom >= 768:
            game_over = True
            flying = False

        if game_over == False and flying == True:
            time_now = pygame.time.get_ticks()
            if time_now - last_pipe > pipe_frequency:
                pipe_height = random.randint(-pipe_gap // 2, pipe_gap // 2)
                btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height + pipe_gap // 2, -1)
                top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height - pipe_gap // 2, 1)
                pipe_group.add(btm_pipe)
                pipe_group.add(top_pipe)
                last_pipe = time_now
            ground_scroll -= scroll_speed
            if abs(ground_scroll) > 35:
                ground_scroll = 0
            pipe_group.update()
            

        if game_over == True:
            if menu_button.draw() == True:
                button.disabled = True
                main_menu()
            if button.draw() == True:
                start_level5()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
                flying = True

        pygame.display.update()


def endless_level():
    button.disabled = False
    global flying, game_over, score, ground_scroll, last_pipe, pass_pipe
    flying = True
    game_over = False
    score = reset_game()
    pipe_frequency = 2400
    pipe_gap = 170


    while True:
        clock.tick(fps)
        screen.blit(bg, (0, 0))
        bird_group.draw(screen)
        bird_group.update()
        pipe_group.draw(screen)
        screen.blit(ground_img, (ground_scroll, 768))

        if len(pipe_group) > 0:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
                    and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right \
                    and pass_pipe == False:
                pass_pipe = True
            if pass_pipe == True:
                if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                    score += 1
                    pass_pipe = False

        draw_text(str(score), font, white, int(screen_width / 2.1), 20)
        if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
            game_over = True
        if flappy.rect.bottom >= 768:
            game_over = True
            flying = False

        if game_over == False and flying == True:
            time_now = pygame.time.get_ticks()
            if time_now - last_pipe > pipe_frequency:
                pipe_height = random.randint(-pipe_gap // 2, pipe_gap // 2)
                btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height + pipe_gap // 2, -1)
                top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height - pipe_gap // 2, 1)
                pipe_group.add(btm_pipe)
                pipe_group.add(top_pipe)
                last_pipe = time_now
            ground_scroll -= scroll_speed
            if abs(ground_scroll) > 35:
                ground_scroll = 0
            pipe_group.update()

        if game_over == True:
            if menu_button.draw() == True:
                button.disabled = True
                main_menu()
            if button.draw() == True:
                start_level1()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
                flying = True

        pygame.display.update()




def main_menu():
    pygame.display.set_caption('Menu')
    while True:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    endless_button_x = screen_width // 2 - endless_button.get_width() // 2
                    endless_button_y = screen_height // 2 - endless_button.get_height() // 2
                    endless_button_rect = endless_button.get_rect(topleft=(endless_button_x, endless_button_y))

                    if endless_button_rect.collidepoint(mouse_x, mouse_y):
                        game_over = False
                        endless_level()
                        

                    quit_button_x = screen_width // 2 - quit_button.get_width() // 2
                    quit_button_y = screen_height // 1.4 - quit_button.get_height() // 2
                    quit_button_rect = quit_button.get_rect(topleft=(quit_button_x, quit_button_y))

                    if quit_button_rect.collidepoint(mouse_x, mouse_y):
                        pygame.quit()
                        exit()

                    levels_button_x = screen_width // 2 - levels_button.get_width() // 2
                    levels_button_y = screen_height // 1.65 - levels_button.get_height() // 2
                    levels_button_rect = levels_button.get_rect(topleft=(levels_button_x, levels_button_y))

                    if levels_button_rect.collidepoint(mouse_x, mouse_y):
                        levels_menu()
                      
                    anglictina_x = screen_width // 2.6 - anglictina.get_width() // 2
                    anglictina_y = screen_height // 1.1 - anglictina.get_height() // 2
                    anglictina_button_rect = anglictina.get_rect(topleft=(anglictina_x, anglictina_y))

                    if anglictina_button_rect.collidepoint(mouse_x,mouse_y):
                        hra_po_anglicky()

                    madarcina_x = screen_width // 1.6 - madarcina.get_width() // 2
                    madarcina_y = screen_height // 1.1 - madarcina.get_height() // 2
                    madarcina_button_rect = madarcina.get_rect(topleft=(madarcina_x, madarcina_y))

                    if madarcina_button_rect.collidepoint(mouse_x, mouse_y):
                        hra_po_madarsky()


        screen.blit(bg, (0, 0))

        MENU_TEXT = menu_font.render('Flappy Bird', True, '#111111')
        screen.blit(MENU_TEXT, (screen_width // 2 - MENU_TEXT.get_width() // 2, screen_height // 6 - MENU_TEXT.get_height() // 2))
        endless_button_x = screen_width // 2 - endless_button.get_width() // 2
        endless_button_y = screen_height // 2 - endless_button.get_height() // 2
        screen.blit(endless_button, (endless_button_x, endless_button_y))

        quit_button_x = screen_width // 2 - quit_button.get_width() // 2
        quit_button_y = screen_height // 1.4 - quit_button.get_height() // 2
        screen.blit(quit_button, (quit_button_x, quit_button_y))

        levels_button_x = screen_width // 2 - levels_button.get_width() // 2
        levels_button_y = screen_height // 1.65 - levels_button.get_height() // 2
        screen.blit(levels_button, (levels_button_x, levels_button_y))

        anglictina_x = screen_width // 2.6 - anglictina.get_width() // 2
        anglictina_y = screen_height // 1.1 - anglictina.get_height() // 2
        screen.blit(anglictina, (anglictina_x, anglictina_y))

        madarcina_x = screen_width // 1.6 - madarcina.get_width() // 2
        madarcina_y = screen_height // 1.1 - madarcina.get_height() // 2
        screen.blit(madarcina, (madarcina_x, madarcina_y))
        pygame.display.update()
        clock.tick(fps)



def levels_menu():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    menu_button_x = screen_width // 2 - menu_img.get_width() // 2
                    menu_button_y = screen_height // 1.4 - menu_img.get_height() // 2

                    if menu_button_x < mouse_x < menu_button_x + menu_img.get_width() and \
                            menu_button_y < mouse_y < menu_button_y + menu_img.get_height():
                        return  # Exit the levels_menu() function and return to the main_menu()

                    level1_button_x = screen_width // 4.55 - level1.get_width() // 2
                    level1_button_y = screen_height // 2 - level1.get_height() // 2
                    level1_button_rect = level1.get_rect(topleft=(level1_button_x, level1_button_y))

                    if level1_button_rect.collidepoint(mouse_x, mouse_y):
                        start_level1()

                    level2_button_x = level1_button_x + level1.get_width() + (screen_width // 10 - level2.get_width() // 2)
                    level2_button_y = level1_button_y
                    level2_button_rect = level2.get_rect(topleft=(level2_button_x, level2_button_y))

                    if level2_button_rect.collidepoint(mouse_x, mouse_y):
                        start_level2()

                    level3_button_x = level2_button_x + level3.get_width() + (screen_width // 10 - level3.get_width() // 2)
                    level3_button_y = level2_button_y
                    level3_button_rect = level3.get_rect(topleft=(level3_button_x, level3_button_y))

                    if level3_button_rect.collidepoint(mouse_x, mouse_y):
                        start_level3()

                    level4_button_x = level3_button_x + level3.get_width() + (screen_width // 10 - level4.get_width() // 2)
                    level4_button_y = level3_button_y
                    level4_button_rect = level4.get_rect(topleft=(level4_button_x, level4_button_y))

                    if level4_button_rect.collidepoint(mouse_x, mouse_y):
                        start_level4()

                    level5_button_x = level4_button_x + level4.get_width() + (screen_width // 10 - level5.get_width() // 2)
                    level5_button_y = level4_button_y
                    level5_button_rect = level5.get_rect(topleft=(level5_button_x, level5_button_y))

                    if level5_button_rect.collidepoint(mouse_x, mouse_y):
                        start_level5()



        screen.blit(bg, (0, 0))
        draw_text("Levels", font, (0, 0, 0), screen_width // 2.5, screen_height // 8)
        menu_button_x = screen_width // 2 - menu_img.get_width() // 2
        menu_button_y = screen_height // 1.4 - menu_img.get_height() // 2
        screen.blit(menu_img, (menu_button_x, menu_button_y))

        level1_x = screen_width // 4.55 - level1.get_width() // 2
        level1_y = screen_height // 2 - level1.get_height() // 2
        screen.blit(level1, (level1_x, level1_y))

        level2_x = level1_x + level1.get_width() + (screen_width // 10 - level2.get_width() // 2)
        level2_y = level1_y
        screen.blit(level2, (level2_x, level2_y))

        level3_x = level2_x + level2.get_width() + (screen_width // 10 - level3.get_width() // 2)
        level3_y = level1_y
        screen.blit(level3, (level3_x, level3_y))

        level4_x = level3_x + level3.get_width() + (screen_width // 10 - level4.get_width() // 2)
        level4_y = level1_y
        screen.blit(level4, (level4_x, level4_y))

        level5_x = level4_x + level4.get_width() + (screen_width // 10 - level5.get_width() // 2)
        level5_y = level1_y
        screen.blit(level5, (level5_x, level5_y))
        pygame.display.update()
        clock.tick(fps)


hra_po_anglicky()





run = True
while run:
    clock.tick(fps)
    screen.blit(bg, (0,0))
    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)
    screen.blit(ground_img, (ground_scroll , 768))
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False

    draw_text(str(score), font, white, int(screen_width/2.1), 20)              
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True
    if flappy.rect.bottom >= 768:
        game_over = True
        flying = False

    if game_over == False and flying == True:
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100,100)
            btm_pipe=Pipe(screen_width,int(screen_height / 2) + pipe_height,-1)
            top_pipe=Pipe(screen_width,int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0
        pipe_group.update()
    if game_over == True:
        button.disabled = False
        if menu_button.draw() == True:
            main_menu()
        if button.draw() == True:
            button.disabled = True
            start_game()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True
    pygame.display.update()
pygame.quit()
