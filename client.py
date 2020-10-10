import pygame
import random
import math
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
        self.vel = 5

    def draw(self, dis):
        pygame.draw.rect(dis, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if self.y > 0:
            if keys[pygame.K_UP]:
                self.y -= self.vel
        if self.y < 450:
            if keys[pygame.K_DOWN]:
                self.y += self.vel

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)


class Ball():
    """Class for the ball of a pong game"""

    def __init__(self, radius, color):
        self.x = 0
        self.y = 0
        self.ball_pos = (self.x, self.y)
        self.radius = radius
        self.color = color
        self.direction = 0
        self.speed = 0

    def draw(self, dis):
        pygame.draw.circle(dis, self.color, self.ball_pos, self.radius)

    def reset(self):
        self.x = random.randint(80, 320)
        self.y = 250
        self.speed = 5

        # Direction of ball (in degrees)
        self.direction = random.randrange(-45, 45)

        # Flip a 'coin'
        if random.randrange(2) == 0:
            # Reverse ball direction, let the other guy get it first
            self.direction += 180
            self.y = 50
        self.update_ball()

    def bounce(self, diff):
        # This function will bounce the ball off a horizontal surface (not a vertical one)
        self.direction = (180 - self.direction) % 360
        self.direction -= diff

        # Speed the ball up
        self.speed *= 1.1

    def move_ball(self):
        if self.y == 0 + self.radius:
            self.bounce(0)
        if self.y == 500 - self.radius:
            self.bounce(0)
        # Sine and Cosine work in degrees, so we have to convert them
        direction_radians = math.radians(self.direction)

        # Change the position (x and y) according to the speed and direction
        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)

        if self.x < 0:
            self.reset()

        if self.x > 500:
            self.reset()

        self.update_ball()

    def update_ball(self):
        self.ball_pos = (int(self.x), int(self.y))


def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


def redrawWindow(dis, player, player2, ball):
    dis.fill((0, 0, 0))
    player.draw(dis)
    player2.draw(dis)
    ball.draw(dis)
    pygame.display.update()


def main():
    """Draw the players to the screen"""
    n = Network()
    start_pos = read_pos(n.get_pos())
    run = True
    player = Player(start_pos[0], start_pos[1], 50, 50, (250, 250, 250))
    player2 = Player(0, 0, 50, 50, (250, 250, 250))
    ball = Ball(10, (0, 250, 0))
    clock = pygame.time.Clock()
    ball.reset()

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
        ball.move_ball()
        redrawWindow(dis, player, player2, ball)


main()
