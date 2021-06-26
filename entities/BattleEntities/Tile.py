import os

import pygame

TILESET = pygame.image.load(os.path.join("assets", "tiles.png"))


class Tile(pygame.sprite.Sprite):
    def __init__(self, tileNumber, grid_position):
        super().__init__()
        self.surf = pygame.Surface((16, 16))
        self.surf.fill((255, 0, 0))
        self.set_sprite(tileNumber)
        self.grid_position = grid_position
        self.start_position = grid_position
        self.position = (grid_position.x * 16, grid_position.y * 16)
        self.static = True
        self.priority = 100
        self.blocking = True

    def set_sprite(self, tileNumber):
        self.rect = pygame.Rect(tileNumber * 16, 0, 16, 16)
        self.image = pygame.Surface(self.rect.size).convert()
        self.image.blit(TILESET.convert(), (0, 0), self.rect)

    def set_position(self, grid_position):
        self.grid_position = grid_position
        self.position = self.grid_position * 16


class Brick(Tile):
    def __init__(self, position):
        super().__init__(0, position)


class Box(Tile):
    def __init__(self, position):
        super().__init__(3, position)
        self.static = False
        self.blocking = False

    def push(self, grid_position):
        self.set_position(grid_position)

    def set_on_goal_sprite(self):
        self.set_sprite(1)

    def set_standard_sprite(self):
        self.set_sprite(3)


class Goal(Tile):
    def __init__(self, position):
        super().__init__(2, position)
        self.blocking = False
        self.priority = 2


class Floor(Tile):
    def __init__(self, position):
        super().__init__(4, position)
        self.blocking = False
        self.priority = 1
