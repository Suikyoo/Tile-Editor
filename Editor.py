import pygame, sys
from configuration import *
from tileTypes import *
from menu import Menu
from menu import Button
from functions import *
from world import World
mainClock = pygame.time.Clock()
DrawSurf = pygame.Surface((CHUNK_DIMENSION[0] * CHUNK_SIZE[0] * TILE_SIZE[0], CHUNK_DIMENSION[1] * CHUNK_SIZE[1] * TILE_SIZE[1]))
Zoom = 1
drawSurfRect = pygame.Rect(DrawSurf.get_rect())
surfCoords = [400, 0]
world = World()
sideMenu = Menu([0, 0], [390, 900])
def main_loop():
    global Zoom, DrawSurf
    while True:
        dt = mainClock.tick(60)/1000 * 60
        mainTile = sideMenu.return_id()
        keys = pygame.key.get_pressed()
        shift = keys[pygame.K_LSHIFT]
        for i in pygame.event.get():
            world.event_handler(i, mainTile)
            sideMenu.event_handler(i, shift)
            if i.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if i.type == pygame.MOUSEBUTTONDOWN:
                if i.button == 4:
                    Zoom += 0.5
                elif i.button == 5:
                    if Zoom >= 0.5:
                        Zoom -= 0.5
        if shift:
            if keys[pygame.K_w]:
                surfCoords[1] += 5 * dt
            elif keys[pygame.K_s]:
                surfCoords[1] -= 5 * dt
            if keys[pygame.K_a]:
                surfCoords[0] += 5 * dt
            elif keys[pygame.K_d]:
                surfCoords[0] -= 5 * dt 
        world.update(DrawSurf, surfCoords, Zoom)
        SCREEN.fill((10, 10, 40))
        SCREEN.blit(pygame.transform.scale(DrawSurf, (int(width(DrawSurf) * Zoom), int(height(DrawSurf) * Zoom))), surfCoords)
        sideMenu.update(SCREEN)
        for i in Button.buttons:
            i.draw()
        world.highlight_layer()
        pygame.display.update()

main_loop()
