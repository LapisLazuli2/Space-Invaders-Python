import pygame
import sys

# Setup
pygame.init()
clock = pygame.time.Clock()


# Main window
SCREEN_WIDTH = 768 / 2  # 3:4 aspect ratio to mimic vertical arcade shooters
SCREEN_HEIGHT = 1024 / 2
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Space Invaders')


# Constants

SHIP_SIZE = 30
SHIP_STARTING_X = SCREEN_WIDTH / 2 - SHIP_SIZE / 2
SHIP_STARTING_Y = SCREEN_HEIGHT - SHIP_SIZE
SHIP = pygame.Rect(SHIP_STARTING_X, SHIP_STARTING_Y, SHIP_SIZE, SHIP_SIZE)
SHIP_SPEED = 1
SHIP_COLOR = pygame.Color("red")

INVADER_SIZE = 30
INVADER_SPAWN_X = SCREEN_WIDTH / 2
INVADER_SPAWN_Y = 0 + INVADER_SIZE * 2
INVADER = pygame.Rect(INVADER_SPAWN_X, INVADER_SPAWN_Y, INVADER_SIZE, INVADER_SIZE)
INVADER_SPEED = 1
INVADER_COLOR = pygame.Color("blue")

BG_COLOR = pygame.Color("grey")

# Junk variable for testing
# refactor all mentions of this
ship_velocity253 = 0

# Functions

def handleInput():
    global ship_velocity253
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                ship_velocity253 -= SHIP_SPEED
            if event.key == pygame.K_RIGHT:
                ship_velocity253 += SHIP_SPEED
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                ship_velocity253 = 0
            if event.key == pygame.K_RIGHT:
                ship_velocity253 = 0


def renderDisplay():
    SCREEN.fill(BG_COLOR)
    # Draw player ship to display
    pygame.draw.rect(SCREEN, SHIP_COLOR, SHIP)
    # Draw invaders to display
    pygame.draw.ellipse(SCREEN, INVADER_COLOR, INVADER)
    # Draw display
    pygame.display.flip()

def tickGame():
    SHIP.x += ship_velocity253
    INVADER.y += INVADER_SPEED

    #Collision detection
    if SHIP.colliderect(INVADER):
        print('Collision!')
 

# Game loop
while True:
    handleInput()
    
    tickGame()

    renderDisplay()
    
    clock.tick(60)



