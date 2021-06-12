import os

import pygame

from core.UI import TextOptionsUIPanel, TextUIOption

from core.statemachine import AbstractState


class SelectState(AbstractState):
    def __init__(self, state_machine):
        super().__init__(state_machine)
        self.surf = None
        self.panel = None
        self.options = []
        self.save_manager = None

    def enter(self, persisted_data, current_time):
        super().enter(persisted_data, current_time)
        self.save_manager = self.state_machine.get_data("SAVE_MANAGER")
        self.save_manager.load()

        self.load_options = []
        index = 0
        for save in self.save_manager.save_data.player_data:
            option_string = "{} L{}".format(
                save.name.ljust(8), str(save.get_next_level())
            )
            self.load_options.append(
                TextUIOption(option_string, index, self._select_player)
            )
            index += 1
        new_player_count = 3 - len(self.load_options)
        for i in range(new_player_count):
            self.load_options.append(
                TextUIOption("NEW", len(self.load_options), self._register_new_player)
            )

        self.load_panel = TextOptionsUIPanel(
            pygame.Vector2(100, 100), self.load_options, "Select a save", 0
        )
        self.surf = pygame.Surface(self.load_panel.size)

    def _select_player(self):
        self.current_player = self.save_manager.save_data.player_data[
            self.load_panel.current_option.position
        ]
        self.data_to_persist["current_player"] = self.current_player
        self.data_to_persist["surfaces"] = self.surf
        self.state_machine.change_state("PLAY_SELECT")

    def _register_new_player(self):
        self.state_machine.change_state("REGISTER")

    def _build_surfaces(self):
        self.surfaces = []
        self.surf.blit(self.load_panel.surf, self.load_panel.screen_position)
        self.surfaces.append({"surface": self.surf, "position": None})

    def _check_save_file_exists():
        pass

    def update(self, current_time):
        super().update(current_time)
        self._build_surfaces()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.load_panel.previous_option()
                if event.key == pygame.K_DOWN:
                    self.load_panel.next_option()
                if event.key == pygame.K_RETURN:
                    self.load_panel.current_option.select()
