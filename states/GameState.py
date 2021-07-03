import pygame
import random

from core.statemachine import AbstractState
from entities.BattleEntities.Movement import WalkingMovement
from entities.BattleEntities.Player import PlayerCursor
from entities.BattleEntities.Entity import Unit
from entities.BattleMap.Map import Map, MapTile, Terrain
from renderables.MapRenderer import MapRenderer

vec = pygame.Vector2


class GameState(AbstractState):
    def __init__(self, state_machine):
        super().__init__(state_machine)
        self.screen_size = None
        self.player_cursor = None
        self.input_vector = None
        self.current_location = None
        self.selected_tile = None
        self.map = None
        pass

    def enter(self, persisted_data, current_time):
        super().enter(persisted_data, current_time)
        self.screen_size = self.state_machine.get_data("SCREEN_SIZE")
        self.player_cursor = PlayerCursor(vec(0, 0))
        self.current_location = vec(0, 0)
        self.map = MapRenderer("test.map")
        self.surfaces.append({"surface": self.map.surface, "position":None})

    def handle_events(self, events):
        self.input_vector = vec(0, 0)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.input_vector = vec(-1, 0)
                if event.key == pygame.K_RIGHT:
                    self.input_vector = vec(1, 0)
                if event.key == pygame.K_UP:
                    self.input_vector = vec(0, -1)
                if event.key == pygame.K_DOWN:
                    self.input_vector = vec(0, 1)

    def update(self, current_time):
        if not self.input_vector == vec(0, 0):
            test_location = self.current_location + self.input_vector
            self.selected_tile = self.map.check_target_location(test_location)
            if self.selected_tile is not None:
                self.current_location = test_location
                print(
                    "{} - {} - {} Entities".format(
                        self.selected_tile.terrain_type,
                        self.selected_tile.grid_location,
                        len(self.selected_tile.get_entities()),
                    )
                )
                self.player_cursor.move(self.current_location)
