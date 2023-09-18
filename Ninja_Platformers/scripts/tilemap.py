class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game # Define the game object
        self.tile_size = tile_size # Define the tile size
        self.tilemap = {} # Grid contains every single tile in the game
        self.offgrid_tiles = [] # Contains the tiles that are not on the grid

        for i in range(10):
            self.tilemap[str(3 + i) + ';10'] = {'type': 'grass', 'variant': 1, 'pos': (3 + i, 10)}
            self.tilemap['10;' + str(5 + i)] = {'type': 'stone', 'variant': 1, 'pos': (10, 5 + i)}       

    def render(self, surf):
        # Render the offgrid tiles
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], tile['pos'])
            
        # Render the tiles
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size))
