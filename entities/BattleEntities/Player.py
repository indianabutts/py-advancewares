import os

import pygame

vec = pygame.math.Vector2


class PlayerCursor:
    def __init__(self, grid_position):
        super().__init__()
        self.grid_position = grid_position
        # self.position = (grid_position.x * 16, grid_position.y * 16)

    def move(self, grid_position):
        self.grid_position = grid_position
        # self.position += grid_position * 16
        print("Cursor Moved to {}".format(self.grid_position))
