import random

import pygame

from entities.BattleMap.Map import Terrain, MapTile, Map

vec = pygame.Vector2


class MapRenderer:
    def __init__(self, filename):
        self.filename = filename
        self.map = self._parse_level_file(self.filename)
        self.height = self.get_height()
        self.width = self.get_width()
        self.surface_size = vec(self.width*32, self.height*32)
        self.surface = pygame.Surface(self.surface_size)
        self._build_surface()

    def _parse_level_file(self, filename):
        map = Map()
        for y in range(10):
            for x in range(10):
                tile = MapTile(vec(x, y), random.choice(list(Terrain)))
                print(tile.terrain_type)
                map.add_tile(tile)
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