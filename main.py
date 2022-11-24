import pygame
from pygame.locals import *

import random
import time
import sys

pygame.init()

# Initialize Images


background = pygame.image.load("Sprites\Background\\Nebula_1_1_Bottom.png")
bgstars = pygame.image.load("Sprites\Background\Stars-Medium_1_1_PC.png")


playerimage = pygame.image.load("Sprites\Player Ships\Short-Lazer-Ship.png")

enemySprite = pygame.image.load("Sprites\Enemies\Enemy_01.png")



# List of stuff
bullets = []
machinebullets = []
enemies = []
enemiespos = []



WIDTH, HEIGHT = 1000, 900


window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plane Shooter")
clock = pygame.time.Clock()

FRAMERATE = 60


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

        self.resizeimage()

    def resizeimage(self) -> None:
        width = self.image.get_rect().width
        height = self.image.get_rect().height

        self.image = pygame.transform.scale(self.image, (int(width * self.resizeFactor), int(height * self.resizeFactor)))

    def Movement(self, pressed: dict) -> None:
        if pressed[pygame.K_a]:
            self.x -= self.vel
        
        if pressed[pygame.K_d]:
            self.x += self.vel

        if pressed[pygame.K_w]:
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

        """ if pressed[pygame.K_w]:
            self.y -= self.vel
        
        if pressed[pygame.K_s]:
            self.y += self.vel"""

    
    def spawnBullet(self):
        Bullet(self.x, self.y)


    def draw(self):     
        return self.surface.blit(self.image, (self.x, self.y))


class Bullet():
    def __init__(self, x , y, xoffset=25, yoffset=70, image=pygame.image.load("Sprites\Weapons\Ball_02.png"), bullet=True, dir=1):
        global bullets
        self.x = x + xoffset
        self.y = y - yoffset
        self.image = image
        self.surface = window
        self.bullet = bullet
        self.dir = dir

        self.vel = 12
        if bullet:
            bullets.append(self)
        else:
            machinebullets.append(self)


    def move(self):
        self.y -= self.vel * self.dir

    def draw(self):
        global bullets
        height = self.image.get_rect().width
        if self.y <= -height:
            bullets.pop(0)
        return self.surface.blit(self.image, (self.x, self.y))




class Enemy:
    def __init__(self, x, y, image=enemySprite, surface=window, resizeFactor=.125, spawnbulletchance=100):
        self.x = x
        self.y = y
        self.image = image
        self.surface = surface
        self.resizeFactor = resizeFactor
        
        self.spawnbulletchance = spawnbulletchance / round

        self.resize()

    def resize(self) -> None:
        width = self.image.get_rect().width
        height = self.image.get_rect().height

        self.image = pygame.transform.scale(self.image, (int(width * self.resizeFactor), int(height * self.resizeFactor)))
    
    def spawnmachinebullet(self) -> None:
        Bullet(self.x, self.y, xoffset=45, yoffset=-70, image=pygame.image.load("Sprites\Weapons\Machine Gun.png"), bullet=False, dir=-1)

    def draw(self):
        shootbullet = random.randint(0, self.spawnbulletchance)

        if shootbullet == self.spawnbulletchance / 2:
            print("shoot")
            self.spawnmachinebullet()

        return self.surface.blit(self.image, (self.x, self.y))


def GenerateEnemies(round):
    global enemies, enemiespos
    numenemies = round * 2 
    for enemy in range(numenemies):
        randomx = 0
        randomy = 0
        randomx = random.randint(0, 600)
        randomy = random.randint(0, 400)
        enemies.append(Enemy(randomx, randomy))






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
while run:
    clock.tick(FRAMERATE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stopGame()

    for bullet in bullets:
        bullet.draw()
        bullet.move()
    

    

    # Handle Movement
    # Not best method of detecting keys
    # Used because will always monitor if key is presseed
    pressed = pygame.key.get_pressed()
    player.Movement(pressed)
    #window.blit(bgstars, (0, 0))    
    window.blit(background, (0, 0))   
    
    player.draw()
    for enemy in enemies:
        enemy.draw()

    for bullet in machinebullets:
        bullet.draw()
        bullet.move()

    pygame.display.flip()