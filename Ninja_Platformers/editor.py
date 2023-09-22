# Base files and classes for the game
# Import depenencies
import sys
import pygame
from scripts.utils import load_images
from scripts.tilemap import Tilemap

RENDER_SCALE = 2.0  # Define the render scale

# Editor class


class Editor:
    # Constructor to initialize the game
    def __init__(self):
        # Initialize pygame
        pygame.init()
        # Change the title of the game
        pygame.display.set_caption("Editor")
        # Defne the screen
        self.screen = pygame.display.set_mode(
            (640, 480))  # Define the screen size
        # Define the surface to render on which will be scaled to screen size for pixel art effect
        self.display = pygame.Surface((320, 240))
        # Define the game clock to force the game to run at a certain fps
        self.clock = pygame.time.Clock()

        # Load the assets
        self.assets = {
            'decor': load_images('tiles/decor'),  # Load the decor image
            'grass': load_images('tiles/grass'),  # Load the grass image
            # Load the large decor image
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),  # Load the stone image
        }

        # Ddefine the movement variable
        self.movement = [False, False, False, False]
        # Define the tilemap
        self.tilemap = Tilemap(self, tile_size=16)
        # Define scroll variables for camera
        self.scroll = [0, 0]

    # Function to run the game loop
    def run(self):
        # Run an infinite loop to keep the game running
        while True:
            # Fill the screen with sky blue color
            self.display.fill((0, 0, 0))
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
                    if event.key == pygame.K_UP:  # Jump
                        self.movement[2] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = True
                # Check if the user released a key
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    if event.key == pygame.K_UP:
                        self.movement[2] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = False

            # Blit the display surface on the screen after scaling
            self.screen.blit(pygame.transform.scale(
                self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()  # Update the screen
            self.clock.tick(60)  # Force the game to run at 60 fps


# Main entry point for the editor
if __name__ == '__main__':
    # Create a editor object
    editor = Editor()
    # Run the editor
    editor.run()
