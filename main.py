import pygame
import sys

pygame.init()

# Initialize Images


background = pygame.image.load("Sprites\Background\\Nebula_1_1_Bottom.png")

playerimage = pygame.image.load("Sprites\Player Ships\Short-Lazer-Ship.png")







WIDTH, HEIGHT = 1000, 900


window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plane Shooter")
clock = pygame.time.Clock()

FRAMERATE = 60


class Player:
    def __init__(self, x, y, surface, image=playerimage, resizeFactor=.175) -> None:
        self.x = x
        self.y = y
        self.surface = surface
        self.color = (255, 255, 255)
        self.rect = pygame.Rect(30, 30, 60, 60)
        self.image = image
        self.resizeFactor = resizeFactor

        self.resizeimage()

    def resizeimage(self) -> None:
        width = self.image.get_rect().width
        height = self.image.get_rect().height

        self.image = pygame.transform.scale(self.image, (int(width * self.resizeFactor), int(height * self.resizeFactor)))

    def draw(self):
        return self.surface.blit(self.image, (self.x, self.y))




def stopGame():
    global run
    pygame.quit()
    run = False
    sys.exit()

# Player starting pos (400, 700)
player = Player(400, 700, window)



run = True
while run:
    clock.tick(FRAMERATE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stopGame()

    # Handle Movement
    pressed = pygame.key.get_presseed()


    window.blit(background, (0, 0))       
    player.draw()

    pygame.display.flip()