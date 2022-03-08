import pygame
from configuration import *
from tileTypes import *
from world import *
class Menu:
    def __init__(self, coords, size):
        self.coords = coords
        self.size = size
        self.surf = pygame.Surface((130, 300))
        self.tilePalette = TilePalette([0, 30], TILE_MATRIX)
    def event_handler(self, event, shift):
        self.tilePalette.event_handler(event, shift)
    def return_id(self):
        return self.tilePalette.tileId
    def draw(self, surf):
        self.surf.fill((10, 20, 40))
        self.tilePalette.update(self.surf)
        surf.blit(pygame.transform.scale(self.surf, (self.size[0], self.size[1])), self.coords)
    def update(self, surf):
        self.draw(surf)

class TilePalette:
    def __init__(self, coords, matrix):
        self.coords = coords
        self.matrix = matrix
        self.access = [0, 0]
        self.chosenTile = self.matrix[self.access[1]][self.access[0]][1]
        self.tileId = self.matrix[self.access[1]][self.access[0]][0]
    def event_handler(self, event, shift):
        if event.type == pygame.KEYDOWN:
            if not shift:
                if event.key == pygame.K_d:
                    self.access[0] += 1
                if event.key == pygame.K_a:
                    self.access[0] -= 1
                if event.key == pygame.K_s:
                    self.access[1] += 1
                if event.key == pygame.K_w:
                    self.access[1] -= 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                self.access = [0, len(self.matrix) - 1]
                
        self.access_tile()
    def access_tile(self):
        if self.access[1] in range(len(self.matrix)):
            if self.access[0] in range(len(self.matrix[self.access[1]])):
                self.chosenTile = self.matrix[self.access[1]][self.access[0]][1]
                self.tileId = self.matrix[self.access[1]][self.access[0]][0]
            else: self.access[0] = 0
        else: self.access[1] = 0
    def show_selection(self, surf):
        pygame.draw.rect(surf, (255, 255, 255), (self.coords[0] + (self.access[0] * TILE_SIZE[0]), self.coords[1] + (self.access[1] * TILE_SIZE[1]), TILE_SIZE[0], TILE_SIZE[1]), 2)
    def draw(self, surf):
        for y in range(len(self.matrix)):
            for x in range(len(self.matrix[y])):
                surf.blit(self.matrix[y][x][1], (self.coords[0] + (x * TILE_SIZE[0]), self.coords[1] + (y * TILE_SIZE[1])))
        self.show_selection(surf)
    def update(self, surf):
        self.draw(surf)

class Button:
    buttons = []
    def __init__(self, text, coords):
        self.rect = pygame.Rect(coords[0], coords[1], 70, 30)
        self.click = False
        self.text = text
        self.width = 2
        Button.buttons.append(self)
    def event_handler(self, event):
        self.click = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.click = True

    def clicked(self):
        return self.click

    def draw(self):
        pygame.draw.rect(SCREEN, (255, 255, 255), self.rect, self.width)
        FONT.render(SCREEN, self.text, (self.rect.x + 5, self.rect.y + 5))