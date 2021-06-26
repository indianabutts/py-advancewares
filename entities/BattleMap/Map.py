import pygame

from enum import Enum

vec = pygame.Vector2

class Terrain(Enum):
    GRASS = 1
    ROAD = 2


class MapTile:
    def __init__(self, grid_location, terrain_type, entities=[]):
        self.grid_location = grid_location
        self.entities = entities
        self.terrain_type = terrain_type

    def add_entity(self,entity):
        self.entities.append(entity)

    def remove_entity(self,entity):
        self.entities.remove(entity)

class Map:
    def __init__(self, tiles=[]):
        self.tiles = {}
        for tile in tiles:
            self.tiles[(tile.grid_location.x, tile.grid_location.y)] = tile

    def add_tile(self, tile):
        self.tiles[(tile.grid_location.x,tile.grid_location.y)] = tile

    def check_target_location(self, grid_location):
        if (grid_location.x, grid_location.y) in self.tiles:
            return self.tiles[(grid_location.x, grid_location.y)]

        return None
