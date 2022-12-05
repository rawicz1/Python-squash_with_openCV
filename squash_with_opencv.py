import numpy
import pygame, pymunk, sys, cv2
#from mediapipe_hands_tracking import HandTracking
import numpy as np

from cvzone.HandTrackingModule import HandDetector
import cv2

pygame.init()

width = 800
height = 600
screen = pygame.display.set_mode((width, height))
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
FPS = 60
space = pymunk.Space()
space.gravity = (0, 100)
l_thick = screen.get_width()//40  #  line thickness
ball_size = screen.get_width()//100
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)
detector = HandDetector(detectionCon=0.8, maxHands=4)

class Ball():
    def __init__(self):
        self.body = pymunk.Body()
        self.body.position = 100, 40
        self.body.velocity = 300,4
        self.shape = pymunk.Circle(self.body, ball_size)
        self.shape.density = 1
        self.shape.elasticity = 1
        space.add(self.body, self.shape)
        self.shape.collision_type = 1

    def draw(self):
        pygame.draw.circle(screen, 'green', self.body.position, ball_size)

    def ball_reset(self):
        if self.body.position.y >= screen.get_width():
            self.body.position = 500, 40
            self.body.velocity = 0, 0

    def ball_reset2(self):
        #self.body.position = 500, 40
        self.body.velocity = -1000, 0

class Wall():
    def __init__(self, p1, p2, collision_number = None):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, p1, p2, l_thick//2)
        self.shape.elasticity = 0.95
        space.add(self.body, self.shape)
        if collision_number:
            self.shape.collision_type = collision_number

    def draw(self):
        pygame.draw.line(screen, 'grey', self.shape.a, self.shape.b, l_thick)

class Player():
    def __init__(self, colour):
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.position = 600, 600
        self.shape = pymunk.Segment(self.body, (0, -30), (0,30), 10)
        self.shape.elasticity = 1.1
        space.add(self.body, self.shape)
        print(self.body.position)
        self.colour = colour

    def draw(self):

        p1 = self.body.local_to_world(self.shape.a)
        p2 = self.body.local_to_world(self.shape.b)
        pygame.draw.line(screen, self.colour, p1, p2, 20)
        #print(self.body.position)

    def move(self, x, y):
        self.body.position = (x, y)



def ball_player_proximity():

    pass

ball = Ball()
player = Player('white')
# to make 5 players i need to enumerate otherwis last player is steered by mouse


wall_top = Wall([0, 0], [screen.get_width(), 0])
wall_left = Wall([0,0], [0, screen.get_height()])
wall_bottom = Wall([0 , screen.get_height()], [screen.get_width(), screen.get_height()])


while True:  # game loop
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type  == pygame.QUIT or keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            player.shape.elasticity = 2
            player.colour = 'red'
        elif event.type == pygame.MOUSEBUTTONUP:
            player.shape.elasticity = 1
            player.colour = 'white'

    success, img = cap.read()
    #print(cv2.getWindowImageRect(img))
    img = cv2.flip(img, 1)

    hands = detector.findHands(img, flipType=False, draw=False)

    img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  #
    img_RGB = np.rot90(img_RGB)
    frame = pygame.surfarray.make_surface(
        img_RGB).convert()  # to convert it to pygame surface, it has no alpha channel in this case
    frame = pygame.transform.flip(frame, True, False)
    screen.blit(frame, (0, 0))
    #screen.fill('black')
    #player = Player('white')
    if hands:
        hand = hands[0]
        x1 = hand['lmList'][8][0]
        y1 = hand['lmList'][8][1]
        x2 = hand['lmList'][4][0]
        if x2 > x1:
            player.shape.elasticity = 2
            player.colour = 'red'
        elif x2 < x1:
            player.shape.elasticity = 1
            player.colour = 'white'

        player.move(x1, y1)
    player.draw()

    ball.draw()
    ball.ball_reset()
    #player.draw()
    #player.move(x1, y1)
    wall_top.draw()
    wall_left.draw()
    wall_bottom.draw()
    ball_player_proximity()
    clock.tick(FPS)
    space.step(1 / FPS)  # to update space simulation"""
    pygame.display.update()

