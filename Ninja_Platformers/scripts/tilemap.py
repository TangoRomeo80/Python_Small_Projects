import pygame

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1) ,(0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)] # The offsets of the neighbors of a tile
PHYSICS_TILES = {'grass', 'stone'} # The tiles which have physics

class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game # Define the game object
        self.tile_size = tile_size # Define the tile size
        self.tilemap = {} # Grid contains every single tile in the game
        self.offgrid_tiles = [] # Contains the tiles that are not on the grid

        for i in range(10):
            self.tilemap[str(3 + i) + ';10'] = {'type': 'grass', 'variant': 1, 'pos': (3 + i, 10)}
            self.tilemap['10;' + str(5 + i)] = {'type': 'stone', 'variant': 1, 'pos': (10, 5 + i)}       

    # Get tiles around player
    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size)) # Get the location of the tile
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    
    # Get all non decorational tiles which have physics around the player
    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects

    def render(self, surf):
        # Render the offgrid tiles
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], tile['pos'])

        # Render the tiles
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size))
