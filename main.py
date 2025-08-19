import pygame
import os, sys
from pygame import mixer
import random
import math


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# Initialize Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('assets/space3.jpg')

# Background Audio
mixer.music.load('assets/space-audio.mp3')
mixer.music.set_volume(0.1)
mixer.music.play(-1, )

# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('assets/ufo.ico')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('assets/player.png')
playerImg = pygame.transform.scale(playerImg, (64, 64))
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
numEnemies = 6

for i in range(numEnemies):
    img = pygame.image.load('assets/enemy.png')
    img = pygame.transform.scale(img, (64, 64))
    enemyImg.append(img)

    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

# Bullet

# Ready -> You cannot see the bullet on the screen.
# Fire -> The bullet is currently moving.

bulletImg = pygame.image.load('assets/image21.png')
bulletImg = pygame.transform.scale(bulletImg, (32, 32))
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)
over_font2 = pygame.font.Font('freesansbold.ttf', 32)

GameOver = False


def show_score(x, y):
    score = font.render('Score: ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over():
    if GameOver == True:
        over = over_font.render('GAME OVER', True, (255, 50, 50))
        over2 = over_font2.render('Press ESC To Play Again.', True, (255, 255, 255))
        screen.blit(over, (200, 250))
        screen.blit(over2, (200, 320))


def player(x, y):
    screen.blit(playerImg, (playerX, playerY))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


# Distance between two points formula.

def collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game loop
running = True
while running:

    # Change screen colour (RGB)
    screen.fill((0, 0, 0,))
    # Adding the BG image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # If keystroke is pressed check if its left or right to move.

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        playerX_change = -0.4

    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        playerX_change = 0.4

    else:
        playerX_change = 0

    if keys[pygame.K_SPACE]:
        if bullet_state == "ready":
            bullet_sound = mixer.Sound('assets/laser-104024.mp3')
            bullet_sound.set_volume(0.1)
            bullet_sound.play()

            bulletX = playerX
            fire(bulletX, bulletY)

    # Player movement

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement

    for i in range(numEnemies):

        # Game Over
        if enemyY[i] > 440:
            GameOver = True
            for j in range(numEnemies):
                enemyY[j] = 2000
            if GameOver == True:
                game_over()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and GameOver == True:
                        GameOver = False
                        print('working')
                        score_value = 0
                        playerX = 370
                        playerY = 480
                        bulletY = 480
                        bullet_state = "ready"

                        enemyX = [random.randint(0, 735) for _ in range(numEnemies)]
                        enemyY = [random.randint(50, 150) for _ in range(numEnemies)]

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[1]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[1]

        iscollision = collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if iscollision:
            collision_sound = mixer.Sound('assets/explosion.wav')
            collision_sound.set_volume(0.1)
            collision_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire(bulletX, bulletY)
        bulletY -= bulletY_change

    # Collision

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
