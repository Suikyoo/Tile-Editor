import pygame, configuration
from functions import cut
def matrify(img, bluePrint, size):
    matrix = []
    id = 0
    for y in range(len(bluePrint)):
        matrix.append([])
        for x in range(bluePrint[y]):
            id += 1
            tile = cut(img, x * size[0], y * size[1], size[0], size[1])
            tile.set_colorkey(configuration.TILE_COLORKEY)
            matrix[y].append([id, tile])
    blankSurf = pygame.Surface((configuration.TILE_SIZE[0], configuration.TILE_SIZE[1]))
    blankSurf.fill((100, 100, 100))
    matrix.append([[0, blankSurf]])
    return matrix


