import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 500, 500

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plane Shooter")
clock = pygame.time.Clock()

FRAMERATE = 60


class Player:
    def __init__(self, x, y, surface) -> None:
        self.x = x
        self.y = y
        self.surface = surface
        self.color = (255, 255, 255)
        self.rect = pygame.Rect(30, 30, 60, 60)


    def draw(self):
        return pygame.draw.rect(self.surface, self.color, self.rect, width=0)




def stopGame():
    global run
    pygame.quit()
    run = False
    sys.exit()

player = Player(20, 30, window)



run = True
while run:
    clock.tick(FRAMERATE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stopGame()
            
    player.draw()

    pygame.display.flip()