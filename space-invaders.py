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
    return g


def renderShip(s):
    """
    renders a ship at the given ship.x and ship.y values
    """
    SHIP.x = s.x
    pygame.draw.rect(SCREEN, SHIP_COLOR, SHIP)


def renderInvaders(invaders):
    """
    Invaders -> Invaders
    renders all the given invaders onto SCREEN
    """
    # !!!
    if len(invaders) < 1:
        return []

def renderDisplay(g):
    """
    renders the ship and all the invaders and missiles within the Game structure
    """
    SCREEN.fill(BG_COLOR)
    
    # Draw player ship to display
    renderShip(g.ship)

    # Draw invaders to display
    # !!!
    #renderInvaders(g.invaders)
    #pygame.draw.ellipse(SCREEN, INVADER_COLOR, INVADER)

    # Draw missiles to display
    # !!!
    #renderMissiles(g.missiles)

    # Draw display
    pygame.display.flip()

def tickShip(s):
    """
    Ship -> Ship
    ticks the given ship by adding ship.x_speed to ship.x
    """
    s.x += s.x_speed
    return s

def tickInvaders(invaders):
    """
    ListOfInvaders -> ListOfInvaders
    ticks each invader by adding INVADER_SPEED to their invader.x and invader.y
    """
    if len(invaders) < 1:
        return []
    else:
        first_invader = tickInvader(invaders[0])
        rest_invaders = tickInvaders(invaders[1:])
        return [first_invader] + rest_invaders 

def tickInvader(invader):
    """
    Invader -> Invader
    ticks the invader by adding INVADER_SPEED to its invader.x and invader.y, and updates the position of the INVADER rect object
    """
    invader.x += invader.x_speed
    invader.y += invader.y_speed
    INVADER.x = invader.x
    INVADER.y = invader.y
    return invader

def tickMissiles(missiles):
    # !!!
    #return missiles
    pass

def tickGame(g):
    #tick Ship
    # !!!
    # Issue: seems like do not need to return values for these functions because they all manipulate the data in the dataclass
    tickShip(g.ship)
    
    #tick Invaders
    g.invaders = tickInvaders(g.invaders)

    #tick Missiles
    #g.missiles = tickMissiles(g.missiles)

    #Collision detection
    if SHIP.colliderect(INVADER):
        print('Collision!')

    return g

# Game loop
def main():
    s = Ship(SHIP_STARTING_X, SHIP_STARTING_Y, 0, 0)
    i = Invader(INVADER_SPAWN_X, INVADER_SPAWN_Y, INVADER_SPEED, INVADER_SPEED)
    i2 = Invader(INVADER_SPAWN_X, INVADER_SPAWN_Y, -INVADER_SPEED, INVADER_SPEED)
    invaders = [i, i2]
    missiles = []
    score = 0
    g = Game(invaders, missiles, s, score)
    """
    !!!
    Issue: how to handle creating multiple on screen invaders? Create a new rect object for each?
           should the rect objects then be part of the dataclasses?
    """
    while True:
        renderDisplay(g)

        handleInput(g)

        tickGame(g)

        clock.tick(60)

main()

