import pygame, json
from configuration import *
from tileTypes import *
from functions import *
import menu
class World:
    def __init__(self):
        self.click = False
        self.pickRect = pygame.Rect(0, 0, 70, 30)
        self.addLayerButton = menu.Button("Add Layer", (5, 50))
        self.maxLayer = 5
        self.layers = [Map()]
        self.currentLayer = self.layers[0]
        self.layerButtons = [menu.Button("Layer 1", (5 + 70 * (len(self.layers) - 1), 10))]
        self.prepare_change  = [None, False]
        if LOAD_MODE: self.load()
        
    def add_layer(self):
        if len(self.layers) < 5:
            map = Map()
            self.layers.append(map)
            self.prepare_change = [map, True]
            self.layerButtons.append(menu.Button("Layer {}".format(len(self.layers)), (len(self.layers) * 5 + 70 * (len(self.layers) - 1), 10)))
    
    def change_layer(self):
        self.currentLayer.preview = True
        self.currentLayer.set_surf()
        self.currentLayer = self.prepare_change[0]
        self.currentLayer.preview = False   
        self.currentLayer.surf = None

    def last_map_update(self, surf, coords, zoom):
        self.currentLayer.update(surf, coords, zoom, True)
        self.change_layer()
        self.prepare_change = [None, False]

    def event_handler(self, event, id):
        self.addLayerButton.event_handler(event)
        self.currentLayer.event_handler(event, id)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.save()
            for index, i in enumerate(self.layers):
                if event.key == pygame.key.key_code(str(index + 1)):
                    self.prepare_change = [i, True]
                  
        if self.addLayerButton.clicked():
            self.add_layer()

    def layer_picker(self):
          self.pickRect.x = ((self.layers.index(self.currentLayer) + 1) * 5 + 70 * self.layers.index(self.currentLayer))
          self.pickRect.y = 10

    def highlight_layer(self):
        self.layer_picker()
        pygame.draw.rect(SCREEN, (255, 255, 255), self.pickRect, 4)
    def draw(self, surf, coords, zoom):
        lst = []
        for i in reversed(self.layers):
            if i != self.currentLayer:
                i.click = False
            if self.prepare_change[1]:
                self.last_map_update(surf, coords, zoom)
            i.update(surf, coords, zoom)
            if i.preview:
                lst.append(self.layers.index(i))

    def update(self, surf, coords, zoom):
        surf.fill(BACKGROUND_COLOR)
        self.draw(surf, coords, zoom)
        
    def save(self):
        chunks = self.flatten()
        saveDict = {
            'map' : chunks,
            'layers' : len(self.layers)
        }
        with open('level.json', 'w') as f:
            json.dump(saveDict, f)
            print('Level Saved')
    
    def load(self):
        with open('level.json', 'r') as f:
            data = json.load(f)
        
        for i in range(data['layers'] - 1):
            self.add_layer()

        for chunkPos in data['map'].keys():
            for tile in data['map'][chunkPos]:
                self.layers[tile[2]].map[chunkPos].tiles[tile[0][1]][tile[0][0]].id = tile[1]
                
    def flatten(self):
        chunks = {}
        indexList = []
        for map in reversed(self.layers):
            for chunkPos in map.map.keys():
                if chunkPos not in indexList:
                    chunks[chunkPos] = []
                    indexList.append(chunkPos)
                for y in range(len(map.map[chunkPos].tiles)):
                    for x, tile in enumerate(map.map[chunkPos].tiles[y]):
                        if tile.id != 0:
                            chunks[chunkPos].append([[x, y], tile.id, self.layers.index(map)])

        return chunks



class Map:
    def __init__(self):
        self.map = self.set_map()
        self.click = False
        self.preview = False
        self.previewSurf = None
        self.surf = None
    def set_map(self):
        dictionary = {}
        for y in range(CHUNK_DIMENSION[1]):
            for x in range(CHUNK_DIMENSION[0]):
                chunk = Chunk((x * (CHUNK_SIZE[0] * TILE_SIZE[0]), y * (CHUNK_SIZE[1] * TILE_SIZE[1])))
                chunk.generate_tiles(CHUNK_SIZE)
                dictionary[str(x) + ":" + str(y)] = chunk
        return dictionary

    def event_handler(self, event, id):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1  or event.button == 3:
                self.click = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1  or event.button == 3:
                self.click = False  
        x, y = pygame.mouse.get_pos()
        for i in self.map.values():
            i.event_handler((x, y), id, self.click)

    def set_surf(self):
        self.previewSurf = cut(self.surf, 0, 0, self.surf.get_width(), self.surf.get_height())
        self.previewSurf.set_colorkey((0, 0, 0))
    def draw(self, surf, coords, zoom):
        for i in self.map.values():
            i.update(surf, coords, zoom)
    def update(self, surf, coords, zoom, end=False):
        if not self.preview:
            self.draw(surf, coords, zoom)
            if end:
                self.surf = surf
        else:
            surf.blit(self.previewSurf, (0, 0))
class Chunk:
    def __init__(self, coords):
        self.coords = pygame.Vector2(coords)
        self.tiles = None
        self.rect = pygame.Rect(self.coords[0], self.coords[1], CHUNK_SIZE[0] * TILE_SIZE[0], CHUNK_SIZE[1] * TILE_SIZE[1])
        self.clicked = False
    def set_tiles(self, matrix):
        self.tiles = matrix
    def generate_tiles(self, dimension):
        lst = []
        for y in range(dimension[1]):
            lst.append([])
            for x in range(dimension[0]):
                lst[y].append(Tile(0, ( self.coords[0] + (x * TILE_SIZE[0]), self.coords[1] + (y * TILE_SIZE[1]))))
        self.set_tiles(lst)
    def event_handler(self, pos, id, click):
        for y in self.tiles:
            for x in y:
                x.event_handler(pos, id, click)

                    
    def draw(self, surf, coords, zoom):
        for y in self.tiles:
            for x in y:
                x.update(surf, coords, zoom)
        pygame.draw.rect(SCREEN, (255, 255, 255), self.rect, 1)
    def update(self, surf, coords, zoom):
        self.draw(surf, coords, zoom)
        self.rect = pygame.Rect(zoom * self.coords[0] + coords[0], zoom * self.coords[1] + coords[1], CHUNK_SIZE[0] * TILE_SIZE[0] * zoom, CHUNK_SIZE[1] * TILE_SIZE[1] * zoom)
class Tile:
    selectedTile = 0
    def __init__(self, id, coords):
        self.id = id
        self.coords = coords
        self.rect = pygame.Rect(self.coords[0], self.coords[1], TILE_SIZE[0], TILE_SIZE[1])
        self.hover = False
    def event_handler(self, pos, id, click):
        if self.rect.collidepoint(pos):
            Tile.selectedTile = id
            if click:
                self.change_id(id)
    def change_id(self, id):
        self.id = id
    def draw(self, surf):
        if self.id != 0:
            surf.blit(TILE_TYPES[self.id], self.coords)
    def update(self, surf, coords, zoom):
        self.draw(surf)
        self.rect = pygame.Rect(zoom * self.coords[0] + coords[0], zoom * self.coords[1] + coords[1], TILE_SIZE[0] * zoom, TILE_SIZE[1] * zoom)
