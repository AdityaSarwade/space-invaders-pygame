import math
import random

from pygame.locals import *
import pygame
from pygame import mixer

import pygame_gui

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('./assets/background.png')

# Sound
mixer.music.load("./assets/background.wav")
#mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('./assets/ufo.png')
pygame.display.set_icon(icon)

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Player
playerImg = pygame.image.load('./assets/player.png')
playerX = 370
playerY = 480
playerX_change = 0

def player(x, y):
    screen.blit(playerImg, (x, y))

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

# create enemies
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('./assets/enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('./assets/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# draw bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

# collision detection, find distance between (x1,y1) and (x2,y2)
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

def set_background():
    global background
    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))

    # Background Image
    screen.blit(background, (0, 0))

def move_bullet():
    global bulletX, bulletY, bullet_state
    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change    

def game_input():
    global running, playerX_change, bulletX, playerX, bulletY
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletSound = mixer.Sound("./assets/laser.wav")
                    bulletSound.play()
                    # Get the current x cordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

def enemy_movement():
    global enemyX, enemyX_change, enemyY, enemyY_change
    # Enemy Movement
    for i in range(num_of_enemies):

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
 
        enemy(enemyX[i], enemyY[i], i)

def collision():
    global num_of_enemies, enemyX, enemyY, bulletX, bulletY, bullet_state, score_value, playerX, playerY, running

    # Check collision with player
    for i in range(num_of_enemies):
        player_collision = isCollision(enemyX[i], enemyY[i], playerX, playerY)
        if player_collision:
            # Game over logic
            running = False
            print("Game Over")

    # Check collision with bullets
    for i in range(num_of_enemies):
        bullet_collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if bullet_collision:
            explosionSound = mixer.Sound("./assets/explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)




# Create a clock to control the frame rate
clock = pygame.time.Clock()

# Function to reset the game state
def reset_game_state():
    global playerX, playerY, playerX_change, score_value, bullet_state, screen

    playerX = 370
    playerY = 480
    playerX_change = 0

    score_value = 0

    bullet_state = "ready"
    
    screen = pygame.display.set_mode((800, 600))

    # Reset enemy positions
    for i in range(num_of_enemies):
        enemyX[i] = random.randint(0, 736)
        enemyY[i] = random.randint(50, 150)

# Function to display the game over screen
def game_over_screen():
    global screen, score_value

    # Display the score
    score_text = font.render("Your Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score_text, (250, 200))
    
    # Create managers for the buttons outside the game loop
    exit_button_manager = pygame_gui.UIManager((800, 600))
    retry_button_manager = pygame_gui.UIManager((800, 600))

    # Create buttons for exit and retry
    exit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((300, 300), (200, 50)),
        text='Exit',
        manager=exit_button_manager
    )

    retry_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((300, 360), (200, 50)),
        text='Retry',
        manager=retry_button_manager
    )

    running_game_over = True  # Variable to control the game over loop

    while running_game_over:
        # Process UI events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == exit_button:
                        return False  # Exit the game
                    elif event.ui_element == retry_button:
                        reset_game_state()  # Reset the game state
                        return True  # Retry the game

            exit_button_manager.process_events(event)
            retry_button_manager.process_events(event)

        # Draw UI elements
        exit_button_manager.update(0.033)  # Update the manager with a time delta
        retry_button_manager.update(0.033)
        exit_button_manager.draw_ui(screen)
        retry_button_manager.draw_ui(screen)

        # Update the display
        pygame.display.flip()
        clock.tick(30)

    return True  # Continue running the game loop


# Game Loop
running = True
while running:
    set_background()
    game_input() 
    enemy_movement()
    collision()
    move_bullet()
    player(playerX, playerY)
    show_score(textX, testY)

    # Check for game over condition
    if not running:
        running = game_over_screen()
    
    pygame.display.update()
    

pygame.quit()