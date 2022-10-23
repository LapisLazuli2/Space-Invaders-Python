import pygame
import sys
from dataclasses import dataclass
from typing import List

# Setup
pygame.init()
clock = pygame.time.Clock()


# Main window
SCREEN_WIDTH  = 768 / 2  # 3:4 aspect ratio to mimic vertical arcade shooters
SCREEN_HEIGHT = 1024 / 2
SCREEN        = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Space Invaders')


# Constants

SHIP_SIZE        = 30
SHIP_STARTING_X  = SCREEN_WIDTH / 2 - SHIP_SIZE / 2
SHIP_STARTING_Y  = SCREEN_HEIGHT - SHIP_SIZE
SHIP             = pygame.Rect(SHIP_STARTING_X, SHIP_STARTING_Y, SHIP_SIZE, SHIP_SIZE)
SHIP_SPEED       = 1
SHIP_COLOR       = pygame.Color("red")

INVADER_SIZE     = 30
INVADER_SPAWN_X  = SCREEN_WIDTH / 2
INVADER_SPAWN_Y  = 0 + INVADER_SIZE * 2
INVADER          = pygame.Rect(INVADER_SPAWN_X, INVADER_SPAWN_Y, INVADER_SIZE, INVADER_SIZE)
INVADER_SPEED    = 1
INVADER_COLOR    = pygame.Color("blue")

MISSILE_SIZE     = 30
MISSILE_SPAWN_Y  = SCREEN_HEIGHT - SHIP_SIZE
MISSILE          = pygame.Rect(0, MISSILE_SPAWN_Y, MISSILE_SIZE, MISSILE_SIZE)
MISSILE_SPEED    = 1
MISSILE_COLOR    = pygame.Color("black")

BG_COLOR         = pygame.Color("grey")


# Data Definitions

@dataclass()
class Ship:
    x:        int = None
    y:        int = None 
    x_speed:  int = None
    y_speed:  int = None

@dataclass()
class Invader:
    x:        int = None
    y:        int = None
    x_speed:  int = None
    y_speed:  int = None

@dataclass()
class Missile:
    x:        int = None
    y:        int = None
    y_speed:  int = None

@dataclass()
class Game:
    invaders: List[Invader]
    missiles: List[Missile]
    ship:     [Ship] = None
    score:    int    = None


# Functions

def handleInput(g):
    """
    if left key is pressed changes the ship's x axis speed by -SHIP_SPEED, if right key is pressed then by +SHIP_SPEED
    if space bar is pressed the ship shoots missiles
    !!!
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                g.ship.x_speed -= SHIP_SPEED
            if event.key == pygame.K_RIGHT:
                g.ship.x_speed += SHIP_SPEED
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                g.ship.x_speed = 0
            if event.key == pygame.K_RIGHT:
                g.ship.x_speed = 0


def renderShip(s):
    """
    renders SHIP onto SCREEN at the given ship.x value
    """
    SHIP.x = s.x
    pygame.draw.rect(SCREEN, SHIP_COLOR, SHIP)


def renderInvaders(invaders):
    """
    renders all the given invaders
    """
    for invader in invaders:
        renderInvader(invader)

def renderInvader(invader):
    """
    renders INVADER onto SCREEN at the given invader.x and invader.y values
    """
    INVADER.x = invader.x
    INVADER.y = invader.y
    pygame.draw.rect(SCREEN, INVADER_COLOR, INVADER)

def renderMissiles(missiles):
    """
    renders all the given missiles onto SCREEN
    """
    for missile in missiles:
        renderMissile(missile)

def renderMissile(missile):
    """
    renders MISSILE onto SCREEN at the given missile.x and missile.y values
    """
    MISSILE.x = missile.x
    MISSILE.y = missile.y
    pygame.draw.rect(SCREEN, MISSILE_COLOR, MISSILE)

def renderDisplay(g):
    """
    renders the ship and all the invaders and missiles within the given Game structure
    """
    SCREEN.fill(BG_COLOR)
    
    renderShip(g.ship)

    renderInvaders(g.invaders)

    renderMissiles(g.missiles)

    # Draw display
    pygame.display.flip()

def tickShip(s):
    """
    ticks the given ship by adding its x_speed to its x value
    """
    s.x += s.x_speed

def tickInvaders(invaders):
    """
    ticks the given list of invaders
    """
    for invader in invaders:
        tickInvader(invader)

def tickInvader(invader):
    """
    ticks the invader by adding its x_speed and y_speed to its x and y values
    """
    invader.x += invader.x_speed
    invader.y += invader.y_speed

def tickMissiles(missiles):
    """
    tick the given list of missiles
    """
    for missile in missiles:
        tickMissile(missile)

def tickMissile(missile):
    """
    ticks the given missile by subtracting its y_speed from its y value
    """
    missile.y -= missile.y_speed

def tickGame(g):

    tickShip(g.ship)
    
    tickInvaders(g.invaders)

    tickMissiles(g.missiles)

    #Collision detection
    if SHIP.colliderect(INVADER):
        print('Collision!')


# Game loop
def main():
    s = Ship(SHIP_STARTING_X, SHIP_STARTING_Y, 0, 0)
    I = Invader(INVADER_SPAWN_X, INVADER_SPAWN_Y, INVADER_SPEED, INVADER_SPEED)
    I2 = Invader(INVADER_SPAWN_X, 200, -INVADER_SPEED, INVADER_SPEED)
    M1 = Missile(SHIP_STARTING_X, MISSILE_SPAWN_Y, MISSILE_SPEED)
    M2 = Missile(SHIP_STARTING_X - 100, MISSILE_SPAWN_Y, MISSILE_SPEED)

    invaders = [I, I2]
    missiles = [M1, M2]
    score = 0
    g = Game(invaders, missiles, s, score)

    while True:
        renderDisplay(g)

        handleInput(g)

        tickGame(g)

        clock.tick(60)

main()

