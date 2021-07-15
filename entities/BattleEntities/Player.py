import os

import pygame

vec = pygame.math.Vector2


class PlayerCursor:
    def __init__(self, grid_position, tilesize):
        super().__init__()
        self.grid_position = None
        self.world_position = None
        self.tilesize = tilesize
        self.move(grid_position)
        self.surface = pygame.Surface(tilesize)
        pygame.draw.rect(self.surface,(255,0,0),pygame.Rect(0,0,tilesize.x,tilesize.y))

    def move(self, grid_position):
        self.grid_position = grid_position
        self.world_position = vec(grid_position.x*self.tilesize.x, grid_position.y*self.tilesize.y)