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
        self.blood_screen = self.get_texture('resources/textures/blood_screen.png', RES)
        self.digit_size = 90
        self.digit_images = [self.get_texture(f'resources/textures/digits/{i}.png', [self.digit_size] * 2)
                             for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))
        self.game_over_image = self.get_texture('resources/textures/game_over.png', RES)
        self.win_image = self.get_texture('resources/textures/win.png', RES)

    # Main raw method
    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_player_health()

    # Method to see the win screen
    def win(self):
        self.screen.blit(self.win_image, (0, 0))

    # Method for game over screen
    def game_over(self):
        self.screen.blit(self.game_over_image, (0, 0))

    # Method to show the player health
    def draw_player_health(self):
        health = str(self.game.player.health)
        for i, char in enumerate(health):
            self.screen.blit(self.digits[char], (i * self.digit_size, 0))
        self.screen.blit(self.digits['10'], ((i + 1) * self.digit_size, 0))

    # Method to show the player damage
    def player_damage(self):
        self.screen.blit(self.blood_screen, (0, 0))

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
        