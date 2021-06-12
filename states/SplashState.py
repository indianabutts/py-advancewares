import os

import pygame

from core.statemachine import AbstractState
from core.Save import SaveManager

SPLASH_IMAGE = pygame.image.load(os.path.join("assets", "splash.png"))


class SplashState(AbstractState):
    def __init__(self, state_machine):
        super().__init__(state_machine)
        self.surf = None
        self.rect = None
        self.image = None
        pass

    def enter(self, persisted_data, current_time):
        super().enter(persisted_data, current_time)
        self.surf = pygame.Surface(SPLASH_IMAGE.get_size())
        self.surf.fill((255, 255, 255))
        self.rect = pygame.Rect(0, 0, self.surf.get_width(), self.surf.get_height())
        self.image = pygame.Surface(self.rect.size).convert()
        self.image.blit(SPLASH_IMAGE.convert(), (0, 0), self.rect)
        self.surfaces.append({"surface": self.image, "position": None})

    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.state_machine.change_state("SELECT")

    def update(self, current_time):
        pass
