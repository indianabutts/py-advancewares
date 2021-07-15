import random
from abc import ABCMeta, abstractmethod

import pygame
import pytmx

from entities.BattleMap.Map import Terrain, MapTile, Map

vec = pygame.Vector2


#TODO: Need to rethink how to structure the baseClass and it's renderer since the Tile is a subset of the Map.
# Could keep a dict of x,y and pull out the image data from that, while keeping the logic inside the MapClass
class Renderer(metaclass=ABCMeta):
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.surface_size = vec(self.width, self.height)
        self.surface = pygame.Surface(self.surface_size)
        self._build_surface()

    @abstractmethod
    def get_width(self):
        pass

    @abstractmethod
    def get_height(self):
        pass

    @abstractmethod
    def _build_surface(self):
        pass


class MapRenderer(Renderer):
    def __init__(self, filename):
        self.filename = filename
        self.tile_sprites = {}
        self.tileset = None
        self.map, self.tilesize = self._parse_level_file(self.filename)
        self.tileset_atlas = pygame.image.load(self.tileset)
        super().__init__(self.tilesize.x*self.map.width,self.tilesize.y*self.map.height)
        pass

    def _parse_level_file(self, filename):
        tiled_map = pytmx.TiledMap("assets/levels/test.tmx")
        map = Map()
        for layer in tiled_map.layers:
            terrain_type = Terrain[layer.name.upper()]
            for x, y, image in layer.tiles():
                map_tile = MapTile(vec(x,y),terrain_type)
                map.add_tile(map_tile)
                if self.tileset is None:
                    self.tileset = image[0]
                self.tile_sprites[(x*tiled_map.tilewidth,y*tiled_map.tileheight)] = image


        # for y in range(10):
        #     for x in range(27):
        #         tile = MapTile(vec(x, y), random.choice(list(Terrain)))
        #         print(tile.terrain_type)
        #         map.add_tile(tile)
        return map, vec(tiled_map.tilewidth,tiled_map.tileheight)

    def get_width(self):
        return self.map.width

    def get_height(self):
        return self.map.height

    def _build_surface(self):
        for pos, image in self.tile_sprites.items():
            if not self.tileset == image[0]:
                self.tileset = image[0]
                self.tileset_atlas = pygame.image.load(self.tileset)
            rect = pygame.Rect(image[1][0],image[1][1],image[1][2],image[1][3])
            flags = image[2]
            blitimage = pygame.Surface(rect.size).convert()
            blitimage.blit(self.tileset_atlas.convert(),(0,0), rect)
            self.surface.blit(pygame.transform.flip(blitimage,flags.flipped_horizontally, flags.flipped_vertically),pos)

    def check_target_location(self, grid_location):
        return self.map.check_target_location(grid_location)