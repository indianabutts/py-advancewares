import pygame

from core.statemachine import AbstractState

vec = pygame.Vector2


class GameState(AbstractState):
    def __init__(self, state_machine):
        super().__init__(state_machine)
        self.screen_size = None
        self.target_location = None
        pass

    def enter(self, persisted_data, current_time):
        super().enter(persisted_data, current_time)
        self.screen_size = self.state_machine.get_data("SCREEN_SIZE")


    def handle_events(self, events):
        self.target_location = vec(0, 0)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.target_location = vec(-1, 0)
                if event.key == pygame.K_RIGHT:
                    self.target_location = vec(1, 0)
                if event.key == pygame.K_UP:
                    self.target_location = vec(0, -1)
                if event.key == pygame.K_DOWN:
                    self.target_location = vec(0, 1)

    def update(self, current_time):
        pass
