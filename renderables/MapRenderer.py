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
        self.map_data = self._parse_level_file(self.filename)
        self.map = self._parse_level_file(self.filename)
        super().__init__()

    def _parse_level_file(self, filename):
        map = Map()
        tiled_map = pytmx.TiledMap("assets/levels/test.tmx")
        for layer in tiled_map.layers:
            terrain_type = Terrain[layer.name.upper()]
            for x, y, image in layer.tiles():
                print((x, y))

        # for y in range(10):
        #     for x in range(27):
        #         tile = MapTile(vec(x, y), random.choice(list(Terrain)))
        #         print(tile.terrain_type)
        #         map.add_tile(tile)
        return map

    def get_width(self):
        return self.map.width

    def get_height(self):
        return self.map.height

    def _build_surface(self):
        for tile in self.map.get_tiles():
            color = None
            if tile.terrain_type == Terrain.GRASS:
                color = (0,255,0)
            elif tile.terrain_type == Terrain.ROAD:
                color = (125,125,125)
            else:
                color = (0,0,255)
            pygame.draw.rect(self.surface,color,(tile.grid_location.x*32,tile.grid_location.y*32,self.surface_size.x,self.surface_size.y))

    def check_target_location(self, grid_location):
        return self.map.check_target_location(grid_location)