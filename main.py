import pygame
from pygame.locals import *

import random
import time
import sys
import threading

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

hitboxes = []
hitboxrects = []



WIDTH, HEIGHT = 1000, 900


window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plane Shooter")
clock = pygame.time.Clock()

FRAMERATE = 60


class hitbox:
    def __init__(self, obj, offset=0, xoffset=0, yoffset=0, machinebullet=False, playerbullet=True) -> None:
        self.obj = obj
        self.offset = offset
        self.xoffset = xoffset
        self.yoffset = yoffset
        self.x = obj.x + self.xoffset
        self.y = obj.y + self.yoffset
        self.width = obj.image.get_rect().width * self.obj.resizeFactor
        self.height = obj.image.get_rect().height * self.obj.resizeFactor - self.offset
        
        
        
        self.rect = pygame.draw.rect(window, (255, 255, 255), pygame.Rect(self.x, self.y, self.width , self.height), 2)

        self.machinebullet = machinebullet
        self.playerbullet = playerbullet
        
        hitboxes.append(self)
        hitboxrects.append(self.rect)

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
        self.hitbox = hitbox(self, offset=20)
        self.hit = False

       

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

        self.hitbox.move()

    def spawnBullet(self):
        Bullet(self.x, self.y)


    def draw(self): 
        self.hitbox.draw()    
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

        self.resizeFactor = .35   # used for compatibility, needs resizefactor to resize for player and enemy
        if self.bullet:
            self.hitbox = hitbox(self, offset=10, xoffset=40, yoffset=47, playerbullet=True)
        else:
            self.hitbox = hitbox(self, offset=-45, xoffset=13, yoffset=20, machinebullet=True)

        self.vel = 12
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
        elif self.y >= HEIGHT + height:
            machinebullets.pop(0)
        return self.surface.blit(self.image, (self.x, self.y))




class Enemy:
    def __init__(self, x, y, image=enemySprite, surface=window, resizeFactor=.125, spawnbulletchance=100):
        self.x = x
        self.y = y
        self.image = image
        self.surface = surface
        self.resizeFactor = resizeFactor
        
        self.hitbox = hitbox(self, offset=0)

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
        self.hitbox.draw()
        if shootbullet == self.spawnbulletchance / 2:
            self.spawnmachinebullet()

        return self.surface.blit(self.image, (self.x, self.y))

    def destroy(self):
        print("Destroy")

def GenerateEnemies(round):
    global enemies, enemiespos
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
    for enemy in enemies:
        enemy.draw()
    player.draw()
    for bullet in machinebullets:
        bullet.draw()
        bullet.move()
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

    
    

    

    # Handle Movement
    # Not best method of detecting keys
    # Used because will always monitor if key is presseed
    pressed = pygame.key.get_pressed()
    player.Movement(pressed)

    # Draw everything
    drawthread = threading.Thread(target=drawAll)
    drawthread.start()
   

    for bullet in machinebullets:
        #print(player.x in range(int(bullet.hitbox.x + bullet.hitbox.width)) and player.y in range(int(bullet.hitbox.y + bullet.hitbox.width))) \
        bulletboxX = bullet.hitbox.x + bullet.hitbox.width
        bulletboxY = bullet.hitbox.y + bullet.hitbox.height
        playerboxX = player.hitbox.x + player.hitbox.width
        playerboxY = player.hitbox.y + player.hitbox.height
        # Essentially will generate a range of x values for the players hitbox and a range of y values of the players hitbox
        # Then will check if the bullet hitbox is in the players hitbox
        #print(f"Player x: {player.x}, range {range(int(bulletboxY))}")
        #print(len(machinebullets))
        collided = player.hitbox.x in range(int(bulletboxX)) and bullet.hitbox.x in range(int(playerboxX)) and bullet.hitbox.y in range(int(playerboxY)) and player.hitbox.y in range(int(bulletboxY))
        if collided:
            player.hit = True
        else:
            player.hit = False

    # Should be refactored later
    # VERY
    for bullet in bullets:
        for enemy in enemies:
            bulletboxX = bullet.hitbox.x + bullet.hitbox.width
            enemyboxX = enemy.hitbox.x + enemy.hitbox.width
            enemyboxY = enemy.hitbox.y + enemy.hitbox.height
            collided = enemy.x in range(int(bulletboxX)) and bullet.hitbox.x in range(int(enemyboxX)) and bullet.hitbox.y in range(int(enemyboxY))
            if collided:
                enemy.destroy()




    print(player.hit)

    
    

    


    pygame.display.flip()