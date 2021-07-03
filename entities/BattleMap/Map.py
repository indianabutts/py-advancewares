import pygame

from enum import Enum

from entities.BattleEntities.Entity import Unit, Building

vec = pygame.Vector2


class Terrain(Enum):
    GRASS = 1
    ROAD = 2
    OCEAN = 3


class MapTile:
    def __init__(self, grid_location, terrain_type, unit=None, building=None):
        self.grid_location = grid_location
        self.unit = unit
        self.building = building
        self.terrain_type = terrain_type

    def add_entity(self, entity):
        if entity is Unit:
            self.unit = entity
            return
        if entity is Building:
            self.building = entity
            return

    def remove_entity(self, entity):
        if entity is Unit:
            self.unit = None
            return
        if entity is Building:
            self.building = None
            return

    def get_entities(self):
        entities = {}
        if self.unit is not None:
            entities["unit"] = self.unit
        if self.building is not None:
            entities["building"] = self.building
        return entities


class Map:
    def __init__(self, tiles=None):
        self.tiles = {}
        self.width = 0
        self.height = 0
        if tiles is not None:
            for tile in tiles:
                self.tiles[(tile.grid_location.x, tile.grid_location.y)] = tile

    def add_tile(self, tile):
        self.tiles[(tile.grid_location.x, tile.grid_location.y)] = tile
        self.width = max(tile.grid_location.x, self.width)
        self.height = max(tile.grid_location.y, self.height)

    def check_target_location(self, grid_location):
        if (grid_location.x, grid_location.y) in self.tiles:
            return self.tiles[(grid_location.x, grid_location.y)]
        return None

    def get_tiles(self):
        return self.tiles.values()