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


class TileSet:
    def __init__(self, filename, tile_size):
        self.filename = filename
        self.atlas = pygame.image.load(self.filename)
        self.tile_size = tile_size

class MapRenderer(Renderer):
    def __init__(self, filename):
        self.filename = filename
        self.tile_sprites = {}
        self.tileset = None
        self.map, self.tilesize = self._parse_level_file(self.filename)
        super().__init__(self.tilesize.x*self.map.width,self.tilesize.y*self.map.height)
        pass

    def _parse_level_file(self, filename):
        tiled_map = pytmx.TiledMap("assets/levels/test.tmx")
        map = Map()
        for count, layer in enumerate(tiled_map.layers):
            terrain_type = Terrain[layer.name.upper()]
            for x, y, image in layer.tiles():
                map_tile = MapTile(vec(x,y),terrain_type)
                map.add_tile(map_tile)
                if self.tileset is None:
                    self.tileset = TileSet(image[0], vec(tiled_map.tilewidth, tiled_map.tileheight))
                if count not in self.tile_sprites:
                    self.tile_sprites[count] = {}
                self.tile_sprites[count][(x*tiled_map.tilewidth,y*tiled_map.tileheight)] = image
        return map, vec(tiled_map.tilewidth,tiled_map.tileheight)

    def get_width(self):
        return self.map.width

    def get_height(self):
        return self.map.height

    def _build_surface(self):
        rendered_positions = []
        for priority in sorted(self.tile_sprites, reverse=True):
            print(priority)
            for pos, image in self.tile_sprites[priority].items():
                if pos in rendered_positions:
                    continue
                rendered_positions.append(pos)
                rect = pygame.Rect(image[1][0], image[1][1], image[1][2], image[1][3])
                flags = image[2]
                blitimage = pygame.Surface(rect.size).convert()
                blitimage.blit(self.tileset.atlas.convert(), (0, 0), rect)
                self.surface.blit(
                    pygame.transform.flip(blitimage, flags.flipped_horizontally, flags.flipped_vertically), pos)

    def check_target_location(self, grid_location):
        return self.map.check_target_location(grid_location)