import os
import pygame

from core.UI import TextOptionsUIPanel, TextUIOption

from core.statemachine import AbstractState


class SelectPlayerOption(AbstractState):
    def __init__(self, state_machine):
        super().__init__(state_machine)
        self.surf = None
        self.background_surf = None
        self.panel = None
        self.options = []
        self.save_manager = None

    def enter(self, persisted_data, current_time):
        super().enter(persisted_data, current_time)
        self.player = self.data_to_persist["current_player"]
        self.save_manager = self.state_machine.get_data("SAVE_MANAGER")
        self.background_surf = self.data_to_persist["surfaces"]
        self.surf = pygame.Surface(pygame.Vector2(100, 80))
        self.options = [
            TextUIOption("Continue", 0, self._continue),
            TextUIOption("Delete", 1, self._delete),
        ]
        self.panel = TextOptionsUIPanel(pygame.Vector2(100, 80), self.options)

    def _build_surfaces(self):
        self.surfaces = []
        self.surfaces.append({"surface": self.background_surf, "position": None})
        self.surf.blit(self.panel.surf, self.panel.screen_position)
        self.surfaces.append({"surface": self.surf, "position": None})

    def _continue(self):
        self.data_to_persist["current_player"] = self.player
        self.data_to_persist["level_to_load"] = self.player.get_next_level()
        self.state_machine.change_state("GAME")

    def _delete(self):
        self.save_manager.delete_player_save(self.player)
        self.state_machine.change_state("SELECT")

    def update(self, current_time):
        super().update(current_time)
        self._build_surfaces()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.panel.previous_option()
                if event.key == pygame.K_DOWN:
                    self.panel.next_option()
                if event.key == pygame.K_RETURN:
                    self.panel.current_option.select()
