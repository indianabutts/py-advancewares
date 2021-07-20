from dataclasses import dataclass

import pygame.surface


@dataclass
class GameSurface:
    surface: pygame.surface.Surface
    position: pygame.Vector2
    priority: int = 5
