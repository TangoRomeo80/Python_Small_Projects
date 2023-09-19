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
        self.collisions = {
            'up': False,
            'down': False,
            'left': False,
            'right': False
        }

    # Create rect for physics entity
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    # function to update the entity every frame
    def update(self, tilemap, movement=(0, 0)):
        # Reset the collisions
        self.collisions = {
            'up': False,
            'down': False,
            'left': False,
            'right': False
        }
        # Update the amount of movement in this frame
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        # Update the position of the entity
        self.pos[0] += frame_movement[0] # Update the x position
        # Update collision in x direction
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                # Check if the entity is moving right or left
                # If moving right, set the right side of the entity to the left side of the tile
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True # Set the right collision to true
                # If moving left, set the left side of the entity to the right side of the tile
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True # Set the left collision to true
                # update position of the entity
                self.pos[0] = entity_rect.x
        
        self.pos[1] += frame_movement[1] # Update the y position
        # Update collision in y direction
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                # Check if the entity is moving right or left
                # If moving right, set the right side of the entity to the left side of the tile
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True # Set the down collision to true
                # If moving left, set the left side of the entity to the right side of the tile
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True # Set the up collision to true
                # update position of the entity
                self.pos[1] = entity_rect.y

        # Update the velocity of the entity
        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

    # Function to render the entity (draw it on the screen)
    def render(self, surf, offset=(0, 0)):
        # Surf denotes the surface on which the entity will be drawn
        # Draw the entity on the surface
        surf.blit(self.game.assets['player'], (self.pos[0] - offset[0], self.pos[1] - offset[1]))
        