import pygame
from network import Network

pygame.init()

width = 500
height = 500
dis = pygame.display.set_mode((width, height))
pygame.display.set_caption('Client')

clientNumber = 0


class Player():
    """Class for the player"""
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.vel = 3

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            self.x += self.vel

        if keys[pygame.K_UP]:
            self.y -= self.vel

        if keys[pygame.K_DOWN]:
            self.y += self.vel

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)


def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


def redrawWindow(dis, player, player2):
    dis.fill((255, 255, 255))
    player.draw(dis)
    player2.draw(dis)
    pygame.display.update()


def main():
    """Draw the players to the screen"""
    n = Network()
    start_pos = read_pos(n.get_pos())
    run = True
    player = Player(start_pos[0], start_pos[1], 100, 100, (0, 250, 0))
    player2 = Player(0, 0, 100, 100, (0, 250, 0))
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        player2_pos = read_pos(n.send(make_pos((player.x, player.y))))
        player2.x = player2_pos[0]
        player2.y = player2_pos[1]
        player2.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        player.move()
        redrawWindow(dis, player, player2)


main()
