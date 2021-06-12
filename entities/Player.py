import os

import pygame

SPRITES = pygame.image.load(os.path.join("assets", "player.png"))
vec = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self, grid_position):
        super().__init__()
        self.surf = pygame.Surface((16, 16))
        self.surf.fill((255, 0, 0))
        self.rect = pygame.Rect(2 * 16, 0, 16, 16)
        self.steps = 0
        self.image = pygame.Surface(self.rect.size).convert()
        self.image.blit(SPRITES.convert(), (0, 0), self.rect)
        self.grid_position = grid_position
        self.start_position = vec(grid_position.x, grid_position.y)
        self.position = (grid_position.x * 16, grid_position.y * 16)
        self.key_pressed = False

    def move(self, grid_position):
        self.grid_position += grid_position
        self.position += grid_position * 16
        self.steps += 1

    def reset_player(self, grid_position=vec(-1, -1)):
        if grid_position == vec(-1, -1):
            self.grid_position = vec(self.start_position.x, self.start_position.y)
        else:
            self.grid_position = grid_position
            self.start_position = vec(grid_position.x, grid_position.y)
        self.position = self.grid_position * 16
        self.steps = 0
