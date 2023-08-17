# Base files and classes for the game
# Import depenencies
import sys
import pygame

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
        # Define the game clock to force the game to run at a certain fps
        self.clock = pygame.time.Clock()

    # Function to run the game loop
    def run(self):
        # Run an infinite loop to keep the game running
        while True:
            # Check for events
            for event in pygame.event.get():
                # Check if the user wants to quit
                if event.type == pygame.QUIT:
                    # Quit the game
                    pygame.quit()
                    sys.exit()

            pygame.display.update() # Update the screen
            self.clock.tick(60) # Force the game to run at 60 fps

# Main entry point for the game
if __name__ == '__main__':
    # Create a game object
    game = Game()
    # Run the game
    game.run()
