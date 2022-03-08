import pygame, tileTypes
from tileSetCutter import matrify
from font import Font
#configuration
SCREEN_SIZE = [1000, 600]
CHUNK_DIMENSION = [10, 5]
CHUNK_SIZE = [8, 8]
TILE_SIZE = [13, 13]
TILESET_IMG = 'tileSet.png'
TILESET_BLUEPRINT = [9, 9, 9, 6]
TILE_COLORKEY = (0, 0, 0)
BACKGROUND_COLOR = (0, 0, 0)
LOAD_MODE = False

#constants
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
FONT = Font('assets/font/small_font.png', 6)
TILE_MATRIX = matrify(pygame.image.load(TILESET_IMG).convert(), TILESET_BLUEPRINT, TILE_SIZE)
TILE_TYPES = tileTypes.set_tile_id(TILE_MATRIX)
CURRENT_TILE_ID = 0
