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
        # Load a sample image
        self.img = pygame.image.load("data/images/clouds/cloud_1.png")
        self.img.set_colorkey((0, 0, 0))
        # Set Image position for movement
        self.img_pos = [160, 260]
        self.movement = [False, False]
        # Define area for collision deteciton
        self.collision_area = pygame.Rect(50, 50, 300, 50)


    # Function to run the game loop
    def run(self):
        # Run an infinite loop to keep the game running
        while True:
            # Fill the screen with sky blue color
            self.screen.fill((14, 219, 248))
            # Get image rectangle
            img_r = pygame.Rect(self.img_pos[0], self.img_pos[1], self.img.get_width(), self.img.get_height())
            if img_r.colliderect(self.collision_area):
                pygame.draw.rect(self.screen, (0, 100, 255), self.collision_area)
            else:
                pygame.draw.rect(self.screen, (0, 50, 155), self.collision_area)
            
            # Update the image position
            self.img_pos[1] += (self.movement[1] - self.movement[0]) * 5
            # Draw the image on the screen
            self.screen.blit(self.img, self.img_pos)

            # Check for events
            for event in pygame.event.get():
                # Check if the user wants to quit
                if event.type == pygame.QUIT:
                    # Quit the game
                    pygame.quit()
                    sys.exit()
                # Check if the user pressed a key
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.movement[0] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = True
                # Check if the user released a key
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.movement[0] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = False


            pygame.display.update() # Update the screen
            self.clock.tick(60) # Force the game to run at 60 fps

# Main entry point for the game
if __name__ == '__main__':
    # Create a game object
    game = Game()
    # Run the game
    game.run()
