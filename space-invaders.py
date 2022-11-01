from operator import truediv
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
SHIP_SPEED       = 2
SHIP_COLOR       = pygame.Color("red")

INVADER_SIZE     = 30
INVADER_SPAWN_X  = SCREEN_WIDTH / 2
INVADER_SPAWN_Y  = 0 + INVADER_SIZE * 2
INVADER          = pygame.Rect(INVADER_SPAWN_X, INVADER_SPAWN_Y, INVADER_SIZE, INVADER_SIZE)
INVADER_SPEED    = 1
INVADER_COLOR    = pygame.Color("blue")

MISSILE_SIZE     = 15
MISSILE_SPAWN_Y  = SCREEN_HEIGHT - SHIP_SIZE * 1.5
MISSILE          = pygame.Rect(0, MISSILE_SPAWN_Y, MISSILE_SIZE/2, MISSILE_SIZE)
MISSILE_SPEED    = 4
MISSILE_COLOR    = pygame.Color("black")

SCORE_FONT_SIZE  = 24
SCORE_FONT       = pygame.font.Font("freesansbold.ttf", SCORE_FONT_SIZE)
SCORE_COLOR      = pygame.Color("red")
SCORE_X          = SCREEN_WIDTH * 0.90
SCORE_Y          = 10    

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
    if left key is pressed changes the ship's x axis speed by -SHIP_SPEED
    if right key is pressed then by +SHIP_SPEED
    if space bar is pressed the ship shoots missiles
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
            if event.key == pygame.K_SPACE:
                shootMissile(g)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                g.ship.x_speed = 0
            if event.key == pygame.K_RIGHT:
                g.ship.x_speed = 0


def shootMissile(g):
    """
    adds a Missile object to the given list of missiles, with the missiles' x = ship's x position, y = MISSILE_SPAWN_Y, and y_speed = MISSILE_SPEED
    !!!
    there can be a max of 4 missiles on screen so only add new missiles if g.missiles has less than 4 missiles
    Issue: add some sort of cooldown to prevent player from shooting walls of missiles
    """
    if len(g.missiles) < 4:
        m = Missile(g.ship.x, MISSILE_SPAWN_Y, MISSILE_SPEED)
        g.missiles.append(m)

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

def renderScore(score):
    """
    renders the given value of score onto SCREEN
    !!!
    Issue: when the amount of digits in score increases it looks visually unpleasnt because the render location doesn't change
    """
    score_surface = SCORE_FONT.render(f"{score}", False, SCORE_COLOR)
    SCREEN.blit(score_surface, (SCORE_X, SCORE_Y))


def renderDisplay(g):
    """
    renders the ship and all the invaders and missiles within the given Game structure
    """
    SCREEN.fill(BG_COLOR)
    
    renderShip(g.ship)

    renderInvaders(g.invaders)

    renderMissiles(g.missiles)

    renderScore(g.score)

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

def checkShipOffscreen(s):
    """
    keeps the ship within the vertical screen boundaries
    if the ship's x < 0 resets it to x = 0 and if ship's x > SCREEN_WIDTH - SHIP_SIZE resets it to x = SCREEN_WIDTH - SHIP_SIZE
    """
    if s.x < 0:
        s.x = 0
    elif s.x > SCREEN_WIDTH - SHIP_SIZE:
        s.x = SCREEN_WIDTH - SHIP_SIZE

def checkInvadersOffscreen(invaders):
    """
    keeps invaders within the vertical screen boundaries
    """
    for invader in invaders:
        checkInvaderOffscreen(invader)

def checkInvaderOffscreen(invader):
    """
    keeps the given invader within the vertical screen boundaries by changing its direction if it touches a boundary
    if invader.x < 0 or invader.x > SCREEN_WIDTH - INVADER_SIZE, then multiply invader.x_speed by -1
    """
    if invader.x < 0 or invader.x > SCREEN_WIDTH - INVADER_SIZE:
        invader.x_speed *= -1

def checkMissilesOffscreen(missiles):
    """
    removes any missiles that go past the top screen boundary
    """
    for missile in missiles:
        if isMissileOffscreen(missile):
            missiles.remove(missile)

def isMissileOffscreen(missile):
    """
    returns true if the given missile.y < 0
    """
    return missile.y < 0

def increaseScore(g):
    """
    increases the player's score by 10
    """
    g.score += 10

def checkMissileHitInvader(g):
    """
    if the x and y of a missile and invader are within INVADER_SIZE/2 of each other, remove both elements from the game, and increase the player's score
    """
    for invader in g.invaders:
        for missile in g.missiles:
            if abs(missile.x - invader.x) < INVADER_SIZE/2 and abs(missile.y - invader.y) < INVADER_SIZE/2:
                g.invaders.remove(invader)
                g.missiles.remove(missile)
                increaseScore(g)

def invaderWins(g):
    """
    if the invader touches the bottom of the screen (invader.y >= SCREEN_HEIGHT) or touches the ship (inv.y == ship.y and both x within SHIP_SIZE/2 of eachother),
    then removes the invader and returns true
    """
    for invader in g.invaders:
        if invader.y >= SCREEN_HEIGHT or (invader.y == g.ship.y and abs(invader.x - g.ship.x) < SHIP_SIZE/2):
            g.invaders.remove(invader)
            return True

def endGame():
    """
    !!!
    To do: ends the game
    """
    print('Game Over!')

def checkCollision(g):
    """
    prevents the ship and invaders from going offscreen, and removes offscreen missiles 
    removes invaders if they are hit by missiles
    ends the game if any invader makes it to the bottom of the screen
    """
    checkShipOffscreen(g.ship)

    checkInvadersOffscreen(g.invaders)

    checkMissilesOffscreen(g.missiles)

    checkMissileHitInvader(g)

    if invaderWins(g):
        endGame()
 
def tickGame(g):

    tickShip(g.ship)
    
    tickInvaders(g.invaders)

    tickMissiles(g.missiles)

    checkCollision(g)

    #print(clock)
 


# Game loop
def main():
    s = Ship(SHIP_STARTING_X, SHIP_STARTING_Y, 0, 0)
    I = Invader(INVADER_SPAWN_X, INVADER_SPAWN_Y, INVADER_SPEED, INVADER_SPEED)
    I2 = Invader(INVADER_SPAWN_X, 200, -INVADER_SPEED, INVADER_SPEED)
    M1 = Missile(SHIP_STARTING_X, MISSILE_SPAWN_Y, MISSILE_SPEED)
    M2 = Missile(SHIP_STARTING_X - 100, MISSILE_SPAWN_Y, MISSILE_SPEED)

    invaders = [I, I2]
    missiles = []
    score = 0
    g = Game(invaders, missiles, s, score)
    # !!! To do: add a function for spawning invaders
    while True:
        renderDisplay(g)

        handleInput(g)

        tickGame(g)

        clock.tick(60)

main()

