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
        self.ray_casting_result = [] # List to store the raycasting result
        self.objects_to_render = [] # List to store the objects to render
        self.textures = self.game.object_renderer.wall_textures

    # Method to get drawing objects
    def get_objects_to_render(self):
        self.objects_to_render = []
        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values

            if proj_height < HEIGHT:
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, proj_height))
                wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
            else:
                texture_height = TEXTURE_SIZE * HEIGHT / proj_height
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), HALF_TEXTURE_SIZE - texture_height // 2,
                    SCALE, texture_height
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, HEIGHT))
                wall_pos = (ray * SCALE, 0)

            self.objects_to_render.append((depth, wall_column, wall_pos))

    # Method to cast a ray
    def ray_cast(self):
        self.ray_casting_result = []
        texture_vert, texture_hor = 1, 1
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

            # depth, texture offset
            if depth_vert < depth_hor:
                depth, texture = depth_vert, texture_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert)
            else:
                depth, texture = depth_hor, texture_hor
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor

            # remove fishbowl effect
            depth *= math.cos(self.game.player.angle - ray_angle)

            # projection of the wall slice
            proj_height = SCREEN_DIST / (depth + 0.0001) # Add a small value to avoid division by 0

            # ray casting result
            self.ray_casting_result.append((depth, proj_height, texture, offset))

            # # Draw walls
            # color = [255 / (1 + depth ** 5 * 0.00002)] * 3
            # pg.draw.rect(
            #     self.game.screen, color,
            #     (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height)
            # )

    # Method to update the raycasting
    def update(self):
        # Call the raycast method
        self.ray_cast()
        # Call the get_objects_to_render method
        self.get_objects_to_render()