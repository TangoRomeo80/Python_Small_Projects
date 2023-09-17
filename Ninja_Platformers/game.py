# Base files and classes for the game
# Import depenencies
import sys
import pygame
from scripts.utils import load_image
from scripts.entities import PhysicsEntity

# Game class
class Game:
    # Constructor to initialize the game
    def __init__(self):
        # Initialize pygame
        pygame.init()
        # Change the title of the game
        pygame.display.set_caption("NINJA TANGO")
        # Defne the screen
        self.screen = pygame.display.set_mode((640, 480)) # Define the screen size
        # Define the surface to render on which will be scaled to screen size for pixel art effect
        self.display = pygame.Surface((320, 240))
        # Define the game clock to force the game to run at a certain fps
        self.clock = pygame.time.Clock()
        # Ddefine the movement variable
        self.movement = [False, False]
        # Load the assets
        self.assets = {
            'player': load_image('entities/player.png')
        }
        # define the player entity
        self.player = PhysicsEntity(self, 'player', (50, 50), (8, 15))

    # Function to run the game loop
    def run(self):
        # Run an infinite loop to keep the game running
        while True:
            # Fill the screen with sky blue color
            self.display.fill((14, 219, 248))

            # Update the player
            self.player.update((self.movement[1] - self.movement[0], 0))
            # Render the player
            self.player.render(self.display)
            # Check for events
            for event in pygame.event.get():
                # Check if the user wants to quit
                if event.type == pygame.QUIT:
                    # Quit the game
                    pygame.quit()
                    sys.exit()
                # Check if the user pressed a key
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                # Check if the user released a key
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)) # Blit the display surface on the screen after scaling
            pygame.display.update() # Update the screen
            self.clock.tick(60) # Force the game to run at 60 fps

# Main entry point for the game
if __name__ == '__main__':
    # Create a game object
    game = Game()
    # Run the game
    game.run()
