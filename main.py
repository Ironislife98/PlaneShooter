from math import ceil

import pygame
from pygame.locals import *

import random
import time
import sys
import threading

pygame.init()
pygame.font.init()

# Initialize Images

background = pygame.image.load("Sprites\Background\\Nebula_1_1_Bottom.png")
bgstars = pygame.image.load("Sprites\Background\Stars-Medium_1_1_PC.png")

playerimage = pygame.image.load("Sprites\Player Ships\Short-Lazer-Ship.png")

enemySprite = pygame.image.load("Sprites\Enemies\Enemy_01.png")

enemyhitanimation = [pygame.image.load("Sprites\VFX\Enemy Hit Effect\Enemy Hit Effect_01.png"), pygame.image.load("Sprites\VFX\Enemy Hit Effect\Enemy Hit Effect_02.png")]


# Lists of stuff
bullets = []
machinebullets = []
enemies = []
animations = []
messages = []

# CONSTANTS
WIDTH, HEIGHT = 1000, 900
FRAMERATE = 60
FONT = pygame.font.SysFont("Fixedsys Regular", 30)


window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plane Shooter")
clock = pygame.time.Clock()



# Classes


class hitbox:
    def __init__(self, obj, offset=0, xoffset=0, yoffset=0, machinebullet=False, playerbullet=False, height=0, width=0) -> None:
        self.obj = obj
        self.offset = offset
        self.xoffset = xoffset
        self.yoffset = yoffset
        self.x = obj.x + self.xoffset
        self.y = obj.y + self.yoffset
        if width == 0 and height == 0:
            self.width = obj.image.get_rect().width * self.obj.resizeFactor
            self.height = obj.image.get_rect().height * self.obj.resizeFactor - self.offset
        else:
            self.width = width
            self.height = height

        self.rect = pygame.draw.rect(window, (255, 255, 255), pygame.Rect(self.x, self.y, self.width, self.height), 2)

        self.machinebullet = machinebullet
        self.playerbullet = playerbullet

    def move(self) -> None:
        self.x = self.obj.x + self.xoffset
        self.y = self.obj.y + self.yoffset

    # Only used for testing
    # Hitboxes should be invisible
    def draw(self) -> None:
        self.rect = pygame.draw.rect(window, (255, 255, 255), pygame.Rect(self.x, self.y, self.width, self.height), 2)


class Player:
    def __init__(self, x, y, surface, image=playerimage, resizeFactor=.175, velocity=12, firewait_time=.125) -> None:
        self.x = x
        self.y = y
        self.surface = surface
        self.image = image
        self.vel = velocity

        self.firerate = firewait_time
        self.fire = False
        self.firetime = None
        self.resizeFactor = resizeFactor
        adjustedwidth = int(self.image.get_rect().width * self.resizeFactor)
        adjustedheight = int(self.image.get_rect().height * self.resizeFactor)
        self.hitbox = hitbox(self, offset=20, width=adjustedwidth, height=adjustedheight)
        self.resizeImage()
        #self.hitbox = hitbox(self)
        self.hit = False

    def resizeImage(self) -> None:
        width = self.image.get_rect().width
        height = self.image.get_rect().height

        self.image = pygame.transform.scale(self.image,
                                            (int(width * self.resizeFactor), int(height * self.resizeFactor)))

    def Movement(self, pressed) -> None:
        if pressed[pygame.K_a]:
            self.x -= self.vel

        if pressed[pygame.K_d]:
            self.x += self.vel

        if pressed[pygame.K_w] and not startingNewRound:
            if not self.fire:
                self.spawnBullet()
                self.firetime = time.time()
                self.fire = True
            else:
                if time.time() - self.firetime >= self.firerate:
                    self.fire = False

        if pressed[pygame.K_RIGHT]:
            if not self.fire:
                self.spawnmachinebullet()
                self.firetime = time.time()
                self.fire = True
            else:
                if time.time() - self.firetime >= self.firerate:
                    self.fire = False

        self.hitbox.move()

    def spawnBullet(self):
        Bullet(self.x, self.y)

    def draw(self):
        self.hitbox.draw()
        return self.surface.blit(self.image, (self.x, self.y))


class Bullet:
    def __init__(self, x, y, xoffset=25, yoffset=70, image=pygame.image.load("Sprites\Weapons\Ball_02.png"),
                 bullet=True, dir=1, vel=12):
        global bullets
        self.x = x + xoffset
        self.y = y - yoffset
        self.image = image
        self.surface = window
        self.bullet = bullet
        self.dir = dir

        self.resizeFactor = .35  # used for compatibility, needs resizefactor to resize for player and enemy
        if self.bullet:
            self.hitbox = hitbox(self, offset=10, xoffset=40, yoffset=47, playerbullet=True)
        else:
            self.hitbox = hitbox(self, offset=-45, xoffset=13, yoffset=20, machinebullet=True)

        self.vel = vel
        if bullet:
            bullets.append(self)
        else:
            machinebullets.append(self)

    def move(self):
        self.y -= self.vel * self.dir
        self.hitbox.move()

    def draw(self):
        global bullets
        self.hitbox.draw()
        height = self.image.get_rect().width
        if self.y <= -height:
            bullets.pop(0)
        elif self.y >= HEIGHT:
            machinebullets.pop(0)
        return self.surface.blit(self.image, (self.x, self.y))


class Enemy:
    def __init__(self, x, y, image=enemySprite, surface=window, resizeFactor=.125):
        self.x = x
        self.y = y
        self.image = image
        self.surface = surface
        self.resizeFactor = resizeFactor

        self.hitbox = hitbox(self, offset=0)

        self.spawnbulletchance = 2 * round + 100

        self.resize()

    def resize(self) -> None:
        width = self.image.get_rect().width
        height = self.image.get_rect().height

        self.image = pygame.transform.scale(self.image,
                                            (int(width * self.resizeFactor), int(height * self.resizeFactor)))

    def spawnmachinebullet(self) -> None:
        Bullet(self.x, self.y, xoffset=45, yoffset=-70, image=pygame.image.load("Sprites\Weapons\Machine Gun.png"),
               bullet=False, dir=-1)

    def setBulletChance(self):
        self.spawnbulletchance = 2 * round + 100

    def draw(self):
        self.setBulletChance()
        shootbullet = random.randint(0, self.spawnbulletchance)
        self.hitbox.draw()
        if shootbullet == self.spawnbulletchance / 2:
            self.spawnmachinebullet()

        return self.surface.blit(self.image, (self.x, self.y))

    def destroy(self):
        enemies.pop(enemies.index(self))
        animation = explodeAnimation(bullets[0].hitbox.x, bullets[0].hitbox.y)
        animation.animate()
        bullets.pop(0)


# Message classes

class Message:
    def __init__(self, x, y, message, duration, doAfter, color=(0, 0, 0), antiAlias=True):
        self.x = x
        self.y = y
        self.message = message
        self.duration = duration
        self.creationTime = time.time()
        self.color = color
        self.antiAlias = antiAlias
        self.messageSurface = FONT.render(self.message, self.antiAlias, self.color)
        self.doAfter = doAfter
        messages.append(self)

    def draw(self):
        if time.time() - self.creationTime >= self.duration:
            messages.pop(messages.index(self))
            self.doAfter()
        else:
            return window.blit(self.messageSurface, (self.x, self.y))


class roundMessage(Message):
    def __init__(self, x, y):
        global round
        super().__init__(x, y, f"Round {round + 1} Begins", 5, self.newRound)
        round += 1

    def newRound(self):
        global startingNewRound
        GenerateEnemies(round=round)
        startingNewRound = False

# Animations

class Animation:
    def __init__(self, x, y, images, repeatTimes=10 , startIndex=0, xoffset=0, yoffset=0):
        self.x = x + xoffset
        self.y = y + yoffset
        self.repeatTimes = repeatTimes
        self.images = images
        self.counter = startIndex
        self.image = self.images[self.counter]
        animations.append(self)

    def animate(self):
        self.draw()
        if self.counter <= self.repeatTimes:        # Repeat for times given
            self.image = self.images[self.counter % len(self.images)]   # % len(self.images) to reset back to 0
            self.counter += 1   # Update counter
        else:
            self.destroy()

    def destroy(self):
        animations.pop(animations.index(self))

    def draw(self):
        return window.blit(self.image, (self.x, self.y))


class explodeAnimation(Animation):
    def __init__(self, x, y):
        super().__init__(x, y, enemyhitanimation, xoffset=-100, yoffset=-200)


# Non-Classes functions

def GenerateEnemies(round):
    numenemies = round * 2
    for enemy in range(numenemies):
        randomx = 0
        randomy = 0
        randomx = random.randint(0, 600)
        randomy = random.randint(0, 400)
        enemies.append(Enemy(randomx, randomy))


def drawAll():
    for bullet in bullets:
        bullet.draw()
        bullet.move()
    window.blit(background, (0, 0))
    window.blit(bgstars, (0, 0))
    for bullet in machinebullets:
        bullet.draw()
        bullet.move()
    for enemy in enemies:
        enemy.draw()
    player.draw()
    for animation in animations:
        animation.animate()
    for message in messages:
        message.draw()


def collisionCheck():
    global player, run, delay
    while run:
        clock.tick(FRAMERATE)
        for bullet in machinebullets:
            collided = (player.hitbox.y < bullet.hitbox.y + bullet.hitbox.height) and bullet.hitbox.x in range(player.hitbox.x, player.hitbox.x + player.hitbox.width)


def genRoundMessage():
    msg = roundMessage(100, 100)


def stopGame():
    global run
    pygame.quit()
    run = False
    sys.exit()


# Player starting pos (400, 700)
player = Player(400, 700, window)

round = 1

GenerateEnemies(round)

run = True
delay = 0

collisionThread = threading.Thread(target=collisionCheck)
collisionThread.start()

startingNewRound = False
while run:
    clock.tick(FRAMERATE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stopGame()

    # Handle Movement
    # Not best method of detecting keys
    # Used because will always monitor if key is pressed
    pressed = pygame.key.get_pressed()
    player.Movement(pressed)

    # Draw everything
    drawAll()

    if enemies == [] and not startingNewRound :
        startingNewRound = True
        genRoundMessage()

    # Should be refactored later
    # VERY IN EFFICIENT
    for bullet in bullets:
        for enemy in enemies:
            bulletboxX = bullet.hitbox.x + bullet.hitbox.width
            enemyboxX = enemy.hitbox.x + enemy.hitbox.width
            enemyboxY = enemy.hitbox.y + enemy.hitbox.height
            collided = enemy.x in range(int(bulletboxX)) and bullet.hitbox.x in range(
                int(enemyboxX)) and bullet.hitbox.y in range(int(enemyboxY))
            if collided:
                enemy.destroy()

    pygame.display.flip()
