import os
import pygame

from core.UI import TextPanel, KeyboardUIPanel

from core.statemachine import AbstractState


class RegisterState(AbstractState):
    def __init__(self, state_machine):
        super().__init__(state_machine)
        self.surf = None
        self.keyboard_panel = None
        self.text_panel = None
        self.save_manager = None

    def enter(self, persisted_data, current_time):
        super().enter(persisted_data, current_time)
        self.save_manager = self.state_machine.get_data("SAVE_MANAGER")
        self.text_panel = TextPanel("        ")
        self.keyboard_panel = KeyboardUIPanel(
            8,
            self._register_name,
            8,
            self.text_panel,
            pygame.Vector2(0, self.text_panel.get_size().y),
        )
        self.text_panel_position = pygame.Vector2(
            x=self.text_panel.get_size().x // 2, y=0
        )
        size = pygame.Vector2(
            self.keyboard_panel.get_size().x,
            self.keyboard_panel.get_size().y + self.text_panel.get_size().y + 16,
        )
        self.surf = pygame.Surface(size)

    def update(self, current_time):
        super().update(current_time)
        self._build_surfaces()

    def _build_surfaces(self):
        self.surfaces = []
        self.surf.fill((255, 255, 255))
        self.keyboard_panel.render()
        self.surf.blit(self.keyboard_panel.surf, self.keyboard_panel.screen_position)
        self.surf.blit(self.text_panel.surf, self.text_panel_position)
        self.surfaces.append({"surface": self.surf, "position": None})

    def _register_name(self):
        self.save_manager.create_player_save(self.text_panel.textUI.text)
        self.state_machine.change_state("SELECT")

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.keyboard_panel.move_left()
                if event.key == pygame.K_RIGHT:
                    self.keyboard_panel.move_right()
                if event.key == pygame.K_DOWN:
                    self.keyboard_panel.move_down()
                if event.key == pygame.K_UP:
                    self.keyboard_panel.move_up()
                if event.key == pygame.K_SPACE:
                    self.keyboard_panel.select()
                if event.key == pygame.K_RETURN:
                    self._register_name()
