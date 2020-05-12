import pygame
from button import Button
import random
import copy

pygame.init()

pygame.display.set_caption('Flappy Bird')

screen_width = 450
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))


class Bird():

    def __init__(self):
        pass

    def show(self, x, y):
        self.y = y
        pygame.draw.circle(screen, (255, 255, 255), (x, y), 15)


class Poles():

    def __init__(self):
        pass

    def show(self, x, y):
        self.x = x
        passingSpace = 150
        pygame.draw.rect(screen, (255, 255, 255),
                         ((x, y), (60, 500)))
        pygame.draw.rect(screen, (255, 255, 255),
                         ((x, -100), (60, (100+y) - passingSpace)))


def randomY():
    return random.randint(200, screen_height - 80)


def show_gameover():
    global screen_height
    global screen_width
    text = pygame.font.Font("freesansbold.ttf", int(screen_height*0.1))
    gameover = text.render("GAME OVER", True, (255, 23, 20))
    screen.blit(gameover, (int(screen_width*0.05), int(screen_height*0.4)))


def show_score(score_count):
    global screen_height
    global screen_width
    text = pygame.font.Font("freesansbold.ttf", int(screen_height*0.1))
    score = text.render(str(score_count), True, (30, 255, 80))
    screen.blit(score, (int(screen_width*0.45), int(screen_height*0.05)))


def collision(birdX, birdY, poleX, poleY):
    if birdY > (poleY-15) and birdX > (poleX-15) and birdX < (poleX+60+15):
        return True
    elif birdY < (poleY-120) and birdX > (poleX-15) and birdX < (poleX+60+15):
        return True
    return False


b = Button(screen, (80, 45, 200), (200, 250, 255),
           (200, 250), (100, 60), "PLAY", 30)
state = 'original'
clicked_play = False

# PLAY BUTTON
while True:
    screen.fill((255, 255, 255))
    b.show()
    for event in pygame.event.get():
        if b.isOverMouse() == True:
            if event.type == pygame.MOUSEBUTTONUP:
                clicked_play = True
            state = 'changed'
        elif b.isOverMouse() == False:
            state = 'original'
        if event.type == pygame.QUIT:
            pygame.quit()
    if state == 'changed':
        b.changeColor((80, 240, 80), (14, 37, 100))
    if clicked_play == True:
        break
    pygame.display.update()


restart = True
while restart:
    # GAME PLAY
    bird = Bird()
    pole1 = Poles()
    pole2 = Poles()
    clock = pygame.time.Clock()
    over = False
    # initial x, y of Bird
    birdX = int(screen_width*0.45)
    birdY = int(screen_height*0.5)
    # initial x, y of poles
    pole1X = screen_width
    pole2X = int(screen_width*1.55)
    pole1Y = randomY()
    pole2Y = randomY()
    # gravity
    gravity = 1
    # initial velocity in y
    vel_y = 0
    # velocity of poles
    vel_pole = -5
    # initial score
    score_count = 0
    # for inner loop breakage
    clicked_replay = False

    while True:
        screen.fill((34, 78, 200))
        clock.tick(20)
        if birdY < -30 or birdY >= screen_height or collision(birdX, birdY, pole1X, pole1Y) or collision(birdX, birdY, pole2X, pole2Y):
            show_score(score_count)
            show_gameover()
            over = True
            # REPLAY BUTTON
            b = Button(screen, (80, 45, 200), (200, 250, 255),
                       (160, 350), (150, 60), "REPLAY", 30)
            state = 'original'
            while True:
                b.show()
                for event in pygame.event.get():
                    if b.isOverMouse() == True:
                        if event.type == pygame.MOUSEBUTTONUP:
                            clicked_replay = True
                        state = 'changed'
                    elif b.isOverMouse() == False:
                        state = 'original'
                    if event.type == pygame.QUIT:
                        pygame.quit()
                if state == 'changed':
                    b.changeColor((80, 240, 80), (14, 37, 100))
                if clicked_replay == True:
                    break
                pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    up_force = -10
                    vel_y += up_force

        # GAME LOGIC
        if clicked_replay == True:
            break
        if over == False:
            pole1X += vel_pole
            pole2X += vel_pole
            birdY += vel_y
            vel_y += gravity

            if (pole1X+60) < birdX and (pole1X+60) > birdX-5:
                score_count += 1

            if (pole2X+60) <= birdX and (pole2X+60) > birdX-5:
                score_count += 1

            if pole1X <= -60:
                pole1X = screen_width
                pole1Y = randomY()

            if pole2X <= -60:
                pole2X = screen_width
                pole2Y = randomY()

            pole1.show(pole1X, pole1Y)
            pole2.show(pole2X, pole2Y)
            show_score(score_count)
            bird.show(birdX, birdY)

        pygame.display.update()
