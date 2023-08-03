# File containing all the classes and methods for object renderer
# Importing the libraries
import pygame as pg
from settings import *

class ObjectRenderer:
    # Initialize the object renderer with game and screen
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture('resources/textures/sky.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0

    # Main raw method
    def draw(self):
        self.draw_background()
        self.render_game_objects()
        # self.draw_player_health()

    # Method to draw the background
    def draw_background(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        # floor
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    # Method to draw the game objects
    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True) # Sort the objects by distance to prevent overlapping
        for epth, image, pos in list_objects:
            self.screen.blit(image, pos)

    # Method to get texture
    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        # Load the texture
        texture = pg.image.load(path).convert_alpha()
        # Scale the texture an return it
        return pg.transform.scale(texture, res)

    # Method to load the wall textures
    def load_wall_textures(self):
        return {
            1: self.get_texture('resources/textures/1.png'),
            2: self.get_texture('resources/textures/2.png'),
            3: self.get_texture('resources/textures/3.png'),
            4: self.get_texture('resources/textures/4.png'),
            5: self.get_texture('resources/textures/5.png'),
        }
        