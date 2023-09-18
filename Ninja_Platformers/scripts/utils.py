import os
import pygame

BASE_IMAGE_PATH = 'data/images/'

# Function to load images
def load_image(path):
    img = pygame.image.load(BASE_IMAGE_PATH + path).convert()
    img.set_colorkey((0, 0, 0)) # Set the black color as transparent
    return img

# Function to load tiles
def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMAGE_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images