import pygame

from core.statemachine import AbstractState


from core.UI import TextOptionsUIPanel, TextPanel, TextUIOption


class LevelCompleteState(AbstractState):
    def __init__(self, state_machine):
        super().__init__(state_machine)
        self.complete_options_panel = None
        self.complete_text_panel = None
        self.complete_score_panel = None
        self.current_save = None
        self.current_level = None
        self.steps = None
        self.surf = None
        self.background_surf = None
        self.options = []
        self.save_manager = None

    def enter(self, persisted_data, current_time):
        super().enter(persisted_data, current_time)
        self.current_save = self.data_to_persist["save_data"]
        self.steps = self.data_to_persist["steps"]
        self.current_level = self.data_to_persist["level_data"]
        self.best_steps = self.current_save.get_best_score_for_level(
            self.current_level.level_number
        )
        self.options = [
            TextUIOption("Next", 0, self._continue),
            TextUIOption("Retry", 1, self._retry),
        ]
        self.background_surf = self.data_to_persist["surfaces"]

        best_string = ""

        if self.best_steps is not None:
            best_string = "Best-{}".format(self.best_steps)

        self.complete_text_panel = TextPanel("Level Complete!")
        self.complete_score_panel = TextPanel(
            "Steps-{} {}".format(self.steps, best_string),
            self.complete_text_panel.get_size(),
            screen_position=pygame.Vector2(0, self.complete_text_panel.get_size().y),
        )

        self.complete_options_panel = TextOptionsUIPanel(
            pygame.Vector2(self.complete_text_panel.get_size().x, 35),
            self.options,
            screen_position=pygame.Vector2(
                0,
                self.complete_text_panel.get_size().y
                + self.complete_score_panel.get_size().y,
            ),
        )

        size = pygame.Vector2(
            x=max(
                self.complete_options_panel.get_size().x,
                self.complete_score_panel.get_size().x,
                self.complete_text_panel.get_size().x,
            ),
            y=self.complete_options_panel.get_size().y
            + self.complete_score_panel.get_size().y
            + self.complete_text_panel.get_size().y,
        )
        self.surf = pygame.Surface(size)
        # self._save()

    def _continue(self):
        self._save()
        self.data_to_persist["level_to_load"] = self.current_save.get_next_level()
        self.data_to_persist["current_player"] = self.current_save
        self.state_machine.change_state("GAME")

    def _save(self):
        self.current_save.upsert_level_data(
            self.current_level.level_name,
            self.current_level.level_number,
            self.steps,
        )
        self.state_machine.get_data("SAVE_MANAGER").save()

    def _retry(self):
        self._save()
        self.data_to_persist["level_to_load"] = self.current_level.level_number
        self.data_to_persist["current_player"] = self.current_save
        self.state_machine.change_state("GAME")

    def update(self, current_time):
        super().update(current_time)
        self._build_surfaces()

    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.complete_options_panel.previous_option()
                if event.key == pygame.K_DOWN:
                    self.complete_options_panel.next_option()
                if event.key == pygame.K_RETURN:
                    self.complete_options_panel.current_option.select()

    def _build_surfaces(self):
        self.surfaces = []
        self.surfaces.append({"surface": self.background_surf, "position": None})
        self.surf.blit(
            self.complete_options_panel.surf,
            self.complete_options_panel.screen_position,
        )
        self.surf.blit(
            self.complete_text_panel.surf, self.complete_text_panel.screen_position
        )
        self.surf.blit(
            self.complete_score_panel.surf, self.complete_score_panel.screen_position
        )
        self.surfaces.append({"surface": self.surf, "position": None})
