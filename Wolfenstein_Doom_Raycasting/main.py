# Main entry point of the game
# Import the libraries
import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *

# Game class to initialize and configure the game
class Game:
    # Constructor to initialize the game
    def __init__(self):
        pg.init() # Initialize pygame
        pg.mouse.set_visible(False) # Hide the mouse cursor
        self.screen = pg.display.set_mode(RES) # Set the screen resolution
        self.clock = pg.time.Clock() # Set the clock
        self.delta_time = 1 # Time that has passed since the last frame
        self.new_game() # Start a new game

    # Method to start new game
    def new_game(self):
        self.map = Map(self) # Create a new map
        self.player = Player(self) # Create a new player
        self.object_renderer = ObjectRenderer(self) # Create a new object renderer
        self.raycasting = Raycasting(self) # Create a new raycasting
        # self.static_sprite = SpriteObject(self) # Create a new sprite object
        # self.animated_sprite = AnimatedSprite(self) # Create a new
        self.object_handler = ObjectHandler(self) # Create a new object handler

    # Method to update the screen
    def update(self):
        self.player.update() # Update the player
        self.raycasting.update() # Update the raycasting
        self.object_handler.update() # Update the object handler
        # self.static_sprite.update() # Update the sprite object
        # self.animated_sprite.update() # Update the animated sprite
        pg.display.flip() # Update the whole screen
        self.delta_time = self.clock.tick(FPS) # Set the frame update
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}') # Set the caption
    
    # Method to paint screen
    def draw(self):
        # self.screen.fill('black') # Will fill the screen with black color, will be removed later
        self.object_renderer.draw() # Draw the objects
        # self.map.draw() # Draw the map
        # self.player.draw() # Draw the player

    # Method to check events and handle events
    def check_events(self):
        for event in pg.event.get():
            # Check for closing the window
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit() # Quit pygame
                sys.exit() # Exit the program

    # Method to run the game
    def run(self):
        # Game loop
        while True:
            self.check_events() # Check for events
            self.update() # Update the screen
            self.draw() # Draw the screen

# Main entry point of the game
if __name__ == '__main__':
    game = Game()
    game.run()
