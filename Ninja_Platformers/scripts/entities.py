# This file will contain classes for the game entities 
# Import dependencies
import pygame



class PhysicsEntity:
    # Initialize the entity
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]

    # function to update the entity every frame
    def update(self, movement=(0, 0)):
        # Update the amount of movement in this frame
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        # Update the position of the entity
        self.pos[0] += frame_movement[0] # Update the x position
        self.pos[1] += frame_movement[1] # Update the y position

    # Function to render the entity (draw it on the screen)
    def render(self, surf):
        # Surf denotes the surface on which the entity will be drawn
        # Draw the entity on the surface
        surf.blit(self.game.assets['player'], self.pos)
        