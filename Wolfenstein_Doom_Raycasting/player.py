# File containing all the classes and methods for player
# Import the libraries
from settings import *
import pygame as pg
import math

# Define the player class
class Player:
    # Constructor to initialize the player class
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        # self.shot = False
        # self.health = PLAYER_MAX_HEALTH
        # self.rel = 0
        # self.health_recovery_delay = 700
        # self.time_prev = pg.time.get_ticks()
        # # diagonal movement correction
        # self.diag_move_corr = 1 / math.sqrt(2)

    # Method to move the player
    def movement(self):
        sin_a = math.sin(self.angle) # Calculate the sin of the angle
        cos_a = math.cos(self.angle) # Calculate the cos of the angle
        dx, dy = 0, 0 # Initialize the dx and dy to 0
        speed = PLAYER_SPEED * self.game.delta_time # Calculate the speed
        speed_sin = speed * sin_a # Calculate the speed sin
        speed_cos = speed * cos_a  # Calculate the speed cos

        keys = pg.key.get_pressed()
        # num_key_pressed = -1
        if keys[pg.K_w]:
            # num_key_pressed += 1
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            # num_key_pressed += 1
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_a]:
            # num_key_pressed += 1
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_d]:
            # num_key_pressed += 1
            dx += -speed_sin
            dy += speed_cos

        # # Update the player position
        # self.x += dx
        # self.y += dy

        # diag move correction
        # if num_key_pressed:
        #     dx *= self.diag_move_corr
        #     dy *= self.diag_move_corr

        # Check for wall collision
        self.check_wall_collision(dx, dy)

        if keys[pg.K_LEFT]:
            self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
        if keys[pg.K_RIGHT]:
            self.angle += PLAYER_ROT_SPEED * self.game.delta_time
        self.angle %= math.tau

    # Method to check the wall
    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    # Method to check the wall collision
    def check_wall_collision(self, dx, dy):
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    # Method to check the player draw and movement
    def draw(self):
        pg.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100),
                    (self.x * 100 + WIDTH * math.cos(self.angle),
                     self.y * 100 + WIDTH * math. sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    #Method to update player state
    def update(self):
        self.movement()

    # Property to get the position of the player
    @property
    def pos(self):
        return self.x, self.y

    # Property to get the position of the player on the map
    @property
    def map_pos(self):
        return int(self.x), int(self.y)

    