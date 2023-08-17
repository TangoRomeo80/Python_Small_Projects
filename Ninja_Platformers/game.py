# Base files and classes for the game
# Import depenencies
import pygame

# Initialize pygame
pygame.init()

# Defne the screen
screen = pygame.display.set_mode((640, 480)) # Define the screen size

# Define the game clock to force the game to run at a certain fps
clock = pygame.time.Clock()