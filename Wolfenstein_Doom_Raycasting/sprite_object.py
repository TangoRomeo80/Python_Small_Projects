# This file will handle the interactive objects of the game loop
# Import the libraries
import pygame as pg
from settings import *
import os
from collections import deque

# Sprite object class
class SpriteObject:
    # Constructor to initialize the sprite object
    def __init__(self, game, path='resources/sprites/static_sprites/candlebra.png', 
                pos=(10.5, 3.5), scale=0.7, shift=0.27):
        self.game = game # Reference to the game
        self.player = game.player # Reference to the player
        self.x, self.y = pos # Position of the sprite object
        self.image = pg.image.load(path).convert_alpha() # Load the image
        self.IMAGE_WIDTH = self.image.get_width() # Width of the image
        self.IMAGE_HALF_WIDTH = self.image.get_width() // 2 # Half width of the image
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height() # Ratio of the image
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1 # Initialize initial values
        self.sprite_half_width = 0
        self.SPRITE_SCALE = scale
        self.SPRITE_HEIGHT_SHIFT = shift

    # Method to get the sprite projection
    def get_sprite_projection(self):
        proj = SCREEN_DIST / self.norm_dist * self.SPRITE_SCALE # Sprite have different in size based on distance
        proj_width, proj_height = proj * self.IMAGE_RATIO, proj # Get the width and height of the sprite

        image = pg.transform.scale(self.image, (proj_width, proj_height)) # Scale the image to the calculated size

        self.sprite_half_width = proj_width // 2 # find the half width of the sprite and ensure does not disappear when center is outside the screen
        height_shift = proj_height * self.SPRITE_HEIGHT_SHIFT
        pos = self.screen_x - self.sprite_half_width, HALF_HEIGHT - proj_height // 2 + height_shift

        self.game.raycasting.objects_to_render.append((self.norm_dist, image, pos)) # Add the sprite to the list of objects to render

    # Method to get the sprite object
    def get_sprite(self):
        # use theta = atan2(y2 - y1, x2 - x1) to get the angle between player and sprite
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        self.dx, self.dy = dx, dy
        self.theta = math.atan2(dy, dx)

        # get number of rays between player and sprite using delta_rays = delta_angle / delta_theta
        delta = self.theta - self.player.angle
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau
        
        delta_rays = delta / DELTA_ANGLE
        self.screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE

        # Get the distance of the sprite and remove fishbowl effect
        self.dist = math.hypot(dx, dy)
        self.norm_dist = self.dist * math.cos(delta)
        # Image culling to show sprite only if visible and close to player for optimizaiton
        if -self.IMAGE_HALF_WIDTH < self.screen_x < (WIDTH + self.IMAGE_HALF_WIDTH) and self.norm_dist > 0.5:
            self.get_sprite_projection()

    # Method to update the sprite object
    def update(self):
        self.get_sprite()

# Animated sprite class extending base sprite object class
class AnimatedSprite(SpriteObject):
    # Constructor to initialize the animated sprite
    def __init__(self, game, path='resources/sprites/animated_sprites/green_light/0.png',
                 pos=(11.5, 3.5), scale=0.8, shift=0.16, animation_time=120):
        super().__init__(game, path, pos, scale, shift) # Call the base class constructor
        self.animation_time = animation_time # Animation time
        self.path = path.rsplit('/', 1)[0] # Get the path of the image
        self.images = self.get_images(self.path)
        self.animation_time_prev = pg.time.get_ticks() # Get the time of the previous animation (FPS)
        self.animation_trigger = False  # Animation trigger

    # Method to update the animated sprite
    def update(self):
        super().update()
        self.check_animation_time()
        self.animate(self.images)

    # Method to animate the sprite
    def animate(self, images):
        if self.animation_trigger: # if trigger is true
            images.rotate(-1) # Rotate the queue of images by one to get next image in frame
            self.image = images[0]

    # Method to check the animation time
    def check_animation_time(self):
        self.animation_trigger = False  # Animation trigger
        time_now = pg.time.get_ticks() # Get the time now
        if time_now - self.animation_time_prev > self.animation_time:
            self.animation_time_prev = time_now # Check if the time now is greater than the animation time
            self.animation_trigger = True

    # Method to get the images
    def get_images(self, path):
        images = deque() # Create a list to store the images
        for file_name in os.listdir(path): # Loop through the files in the path and append to the list
            if os.path.isfile(os.path.join(path, file_name)): # Check if the file is a file
                img = pg.image.load(path + '/' + file_name).convert_alpha() # Load the image
                images.append(img) # Append the image to the list
        return images 