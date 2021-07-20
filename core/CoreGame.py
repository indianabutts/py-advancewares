import sys

import pygame.time
from core.statemachine import StateMachine
from states.GameState import GameState

vec = pygame.Vector2

class CoreGame:
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    SCREEN_SCALE = 2

    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(
            (
                self.SCREEN_WIDTH * self.SCREEN_SCALE,
                self.SCREEN_HEIGHT * self.SCREEN_SCALE,
            )
        )
        self.screen = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.state_machine = StateMachine()
        self.state_machine.register_data("SCREEN_SIZE", self.screen.get_size())
       # self.state_machine.register_data("SAVE_MANAGER", self.save_manager)
        registered_states = {
            "GAME": GameState(self.state_machine)
        }
        self.state_machine.setup_state_machine(
            self.clock.get_time(), registered_states, "GAME"
        )

    def run_game(self):
        """Run the main game loop"""
        while True:
            self._check_events()
            self.update()
            self._render()
            self.clock.tick(60)

    def update(self):
        self.state_machine.update(self.clock.get_time() / 1000)

    def _check_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
        self.state_machine.handle_events(events)

    def _render(self):
        self.screen.fill((255, 255, 255))
        rendered = {}
        for renderable in self.state_machine.current_state.surfaces:
            position = (
                self._center_on_screen(self.screen, renderable.surface)
                if renderable.position is None
                else renderable.position
            )
            self.screen.blit(renderable.surface, position)
        self.window.blit(
            pygame.transform.scale(self.screen, self.window.get_size()), (0, 0)
        )
        pygame.display.flip()

    def _center_on_screen(self, screen, surface):
        return vec(
            (screen.get_width() - surface.get_width()) / 2,
            (screen.get_height() - surface.get_height()) / 2,
        )
