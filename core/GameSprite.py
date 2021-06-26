import os

import pygame

vec = pygame.math.Vector2


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, sprite_atlas, sprite_size, sprite_origin):
        self.sprite_atlas = sprite_atlas
        self.sprite_size = sprite_size
        self.sprite_origin = sprite_origin


class AnimationFrame:
    def __init__(self, game_sprite, frames_to_hold):
        self.game_sprite = game_sprite
        self.frames = frames_to_hold

class Animation:
    def __init__(self, frames=[]):
        self.frames = frames

    def play(self):
        pass

    def pause(self):
        pass

    def append_frame(self, frame):
        self.frames.append(frame)

    def prepend_frame(self, frame):
        self.frames.insert(0, frame)

    def insert_frame_at_index(self, frame, index):
        self.frames.insert(index, frame)
