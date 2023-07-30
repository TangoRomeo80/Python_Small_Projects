# File containing all the classes and methods for raycasting
# Importing the libraries
import pygame as pg
import math
from settings import *

# Define the raycasting class
class Raycasting:
    # Initialize the class with the game object
    def __init__(self, game):
        self.game = game

    # Method to cast a ray
    def ray_cast(self):
        ox, oy = self.game.player.pos # Get the player position
        x_map, y_map = self.game.player.map_pos # Get the player map position

        # Calculate the first or center ray
        ray_angle = self.game.player.angle - HALF_FOV  + .0001 # Add a small value to avoid division by 0
        # For loop to cast all the rays
        for ray in range(NUM_RAYS):
            # Calculate the sin and cos of the ray angle
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            # Check for vertical lines
            # if the cos_a is positive then the ray is facing right and if the cos_a is negative then the ray is facing left
            # So for positive cos_a we need to increment the x_map by 1 and for negative cos_a we need to decrement the x_map by a small value
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)
            # Calculate the depth_vert and y_vert
            depth_vert = (x_vert - ox) / cos_a # Calculate the depth_vert (cos = adj/hyp) => (adj = cos * hyp)
            y_vert = oy + depth_vert * sin_a # Calculate the y_vert (sin = opp/hyp) => (opp = sin * hyp)
            
            delta_depth = dx / cos_a # Calculate the delta_depth (cos = adj/hyp) => (adj = cos * hyp)
            dy = delta_depth * sin_a # Calculate the dy (sin = opp/hyp) => (opp = sin * hyp)
            
            # Cast the ray in cycles based on draw distance
            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.world_map: # Check if the tile_vert is in the world_map
                    texture_vert = self.game.map.world_map[tile_vert]
                    break # Break the loop if the tile_vert is in the world_map
                x_vert += dx # Increment the x_vert
                y_vert += dy # Increment the y_vert
                depth_vert += delta_depth # Increment the depth_vert

            # horizontals
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a

            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            for i in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.world_map:
                    texture_hor = self.game.map.world_map[tile_hor]
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            ray_angle += DELTA_ANGLE # Increment the ray angle

            # Determine the depth
            if depth_vert < depth_hor:
                depth =  depth_vert
            else:
                depth = depth_hor

            # Draw for debugging
            pg.draw.line(self.game.screen, 'yellow', (100 * ox, 100 * oy), (100 * ox + 100 * depth * cos_a, 100 * oy + 100 * depth * sin_a), 2)

    # Method to update the raycasting
    def update(self):
        # Call the raycast method
        self.ray_cast()