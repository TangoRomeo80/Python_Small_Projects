# File containing all the settings functionalities
# Import the libraries
import math

# game settings
# RES = WIDTH, HEIGHT = 1366, 768
RES = WIDTH, HEIGHT = 1600, 900 # Define the screen resolution
# RES = WIDTH, HEIGHT = 1920, 1080
# FPS = 60 # Define the FPS for the game
FPS = 0 # Define the FPS for the game

# initial player settings
PLAYER_POS = 1.5, 5  # mini_map
PLAYER_ANGLE = 0
PLAYER_SPEED = 0.004
PLAYER_ROT_SPEED = 0.002
PLAYER_SIZE_SCALE = 60
# PLAYER_MAX_HEALTH = 100

# Ray casting settings
FOV = math.pi / 3 # Define the field of view
HALF_FOV = FOV / 2 # Define the half of the field of view
NUM_RAYS = WIDTH // 2 # Define the number of rays
HALF_NUM_RAYS = NUM_RAYS // 2 # Define the half of the number of rays
DELTA_ANGLE = FOV / NUM_RAYS # Delta angle is the anngle between two rays
MAX_DEPTH = 20 # Define the max depth or max draw distance