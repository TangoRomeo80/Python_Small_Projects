# Base files and classes for the game
# Import depenencies
import sys
import pygame
from scripts.utils import load_image, load_images, Animation
from scripts.entities import PhysicsEntity, Player
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds

# Game class


class Editor:
    # Constructor to initialize the game
    def __init__(self):
        # Initialize pygame
        pygame.init()
        # Change the title of the game
        pygame.display.set_caption("NINJA TANGO")
        # Defne the screen
        self.screen = pygame.display.set_mode(
            (640, 480))  # Define the screen size
        # Define the surface to render on which will be scaled to screen size for pixel art effect
        self.display = pygame.Surface((320, 240))
        # Define the game clock to force the game to run at a certain fps
        self.clock = pygame.time.Clock()
        # Ddefine the movement variable
        self.movement = [False, False]
        # Load the assets
        self.assets = {
            'decor': load_images('tiles/decor'),  # Load the decor image
            'grass': load_images('tiles/grass'),  # Load the grass image
            # Load the large decor image
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),  # Load the stone image
            # Load the player image
            'player': load_image('entities/player.png'),
            # Load the background image
            'background': load_image('background.png'),
            'clouds': load_images('clouds'),  # Load the clouds images
            # Load the idle animation
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            # Load the run animation
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            # Load the jump animation
            'player/jump': Animation(load_images('entities/player/jump')),
            # Load the slide animation
            'plyer/slide': Animation(load_images('entities/player/slide')),
            # Load the wall slide animation
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),
        }
        # Define the clouds
        self.clouds = Clouds(self.assets['clouds'], count=16)
        # define the player entity
        self.player = Player(self, (50, 50), (8, 15))
        # Define the tilemap
        self.tilemap = Tilemap(self, tile_size=16)
        # Define scroll variables for camera
        self.scroll = [0, 0]

    # Function to run the game loop
    def run(self):
        # Run an infinite loop to keep the game running
        while True:
            # Fill the screen with sky blue color
            self.display.blit(self.assets['background'], (0, 0))
            # Update the scroll
            self.scroll[0] += (self.player.rect().centerx -
                               self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery -
                               self.display.get_height() / 2 - self.scroll[1]) / 30
            # Correct the scroll for fractions
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            # Update the clouds
            self.clouds.update()
            # Render the clouds
            self.clouds.render(self.display, offset=render_scroll)
            # Render the tilemap
            self.tilemap.render(self.display, offset=render_scroll)
            # Update the player
            self.player.update(
                self.tilemap, (self.movement[1] - self.movement[0], 0))
            # Render the player
            self.player.render(self.display, offset=render_scroll)
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
                        self.player.velocity[1] = -3
                # Check if the user released a key
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

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
