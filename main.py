import pygame
import random
import math
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((1000, 500))
# background sound
mixer.music.load('background.wav')
mixer.music.play(-1)
# background
background = pygame.image.load("space.jpg")
pygame.display.set_caption("space fighter")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)
# spaceship
img = pygame.image.load("fff.png")
px = 500
py = 430
px_chg = 0
# enemy
img2 = []
enemyX = []
enemyY = []
ex_chg = []
ey_chg = []
num_enemy = 6
for i in range(num_enemy):
    img2.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(0, 100))
    enemyY.append(random.randint(40, 150))
    ex_chg.append(2)
    ey_chg.append(20)

# bullets
img3 = pygame.image.load("bullet.png")
bX = 0
bY = 420
bx_chg = 0
by_chg = 10
b_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10
# game over
gameText = pygame.font.Font('freesansbold.ttf', 64)


def game_over():
    gatxt = gameText.render("GAME OVER", True, (255, 0, 0))
    screen.blit(gatxt, (300, 200))


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game(x, y):
    screen.blit(img, (x, y))


def enemy(x, y, i):
    screen.blit(img2[i], (x, y))


def fire(x, y):
    global b_state
    b_state = "fire"
    screen.blit(img3, (x + 16, y + 10))


def coll(enemyX, enemyY, bX, bY):
    distance = math.sqrt((math.pow(enemyX - bX, 2)) + (math.pow(enemyY - bY, 2)))
    if distance < 27:
        return True
    else:
        return False


# game loop

running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if key is press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                px_chg = -5
                print("left")
            if event.key == pygame.K_RIGHT:
                px_chg = 5
                print("right")
            if event.key == pygame.K_SPACE:
                if b_state is "ready":
                    b_sound = mixer.Sound('laser.wav')
                    b_sound.play()
                    bX = px
                    fire(bX, bY)
                    print("fire")
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                px_chg = 0

    px += px_chg
    if px <= 0:
        px = 0
    elif px >= 936:
        px = 936
    # enemy
    for i in range(num_enemy):
        # game over
        if enemyY[i] > 350:
            for j in range(num_enemy):
                enemyY[j] = 2000
            game_over()
            break

        enemyX[i] += ex_chg[i]
        if enemyX[i] <= 0:
            ex_chg[i] = 2
            enemyY[i] += ey_chg[i]
        elif enemyX[i] >= 936:
            ex_chg[i] = -2
            enemyY[i] += ey_chg[i]
        # collision
        collision = coll(enemyX[i], enemyY[i], bX, bY)
        if collision:
            c_sound = mixer.Sound('explosion.wav')
            c_sound.play()
            bY = 380
            b_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0, 800)
            enemyY[i] = random.randint(40, 150)

        enemy(enemyX[i], enemyY[i], i)
    # Bullet Movement
    if bY <= 0:
        bY = 380
        b_state = "ready"

    if b_state is "fire":
        fire(bX, bY)
        bY -= by_chg

    game(px, py)
    show_score(textX, textY)
    pygame.display.update()
