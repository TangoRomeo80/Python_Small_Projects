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

        self.action = ''
        self.anim_offset = (-3, -3)
        self.flip = False
        self.set_action('idle')

    # Create rect for physics entity
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    # Function to set the action of the entity
    def set_action(self, action):
        if self.action != action:
            self.action = action
            self.animation = self.game.assets[self.type +
                                              '/' + self.action].copy()

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
        frame_movement = (movement[0] + self.velocity[0],
                          movement[1] + self.velocity[1])
        # Update the position of the entity
        self.pos[0] += frame_movement[0]  # Update the x position
        # Update collision in x direction
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                # Check if the entity is moving right or left
                # If moving right, set the right side of the entity to the left side of the tile
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    # Set the right collision to true
                    self.collisions['right'] = True
                # If moving left, set the left side of the entity to the right side of the tile
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    # Set the left collision to true
                    self.collisions['left'] = True
                # update position of the entity
                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]  # Update the y position
        # Update collision in y direction
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                # Check if the entity is moving right or left
                # If moving right, set the right side of the entity to the left side of the tile
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    # Set the down collision to true
                    self.collisions['down'] = True
                # If moving left, set the left side of the entity to the right side of the tile
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    # Set the up collision to true
                    self.collisions['up'] = True
                # update position of the entity
                self.pos[1] = entity_rect.y

        # Update the flip of the entity
        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True

        # Update the velocity of the entity
        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

        self.animation.update()

    # Function to render the entity (draw it on the screen)
    def render(self, surf, offset=(0, 0)):
        # Surf denotes the surface on which the entity will be drawn
        # Draw the entity on the surface
        # surf.blit(self.game.assets['player'], (self.pos[0] - offset[0], self.pos[1] - offset[1]))
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False),
                  (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))


class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)
        self.air_time += 1
        if self.collisions['down']:
            self.air_time = 0

        if self.air_time > 4:
            self.set_action('jump')
        elif movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')

    
