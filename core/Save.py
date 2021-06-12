from dataclasses import dataclass
from typing import List

import os
import pathlib
import pickle


@dataclass
class LevelData:
    name: str
    number: int
    steps: int


@dataclass
class PlayerSaveData:
    name: str
    completed_levels: List[LevelData]

    def get_last_level(self):

        if len(self.completed_levels) > 0:
            return max(level.number for level in self.completed_levels)
        return 0

    def get_next_level(self):
        return self.get_last_level() + 1

    def get_best_score_for_level(self, level_number):
        for level in self.completed_levels:
            if level.number == level_number:
                return level.steps
            
    def upsert_level_data(self, level_name, level_number, steps):
        for level in self.completed_levels:
            if level.number == level_number:
                if steps < level.steps:
                    level.steps = steps
                    return
        self.completed_levels.append(LevelData(level_name, level_number, steps))


@dataclass
class SaveData:
    player_data: List[PlayerSaveData]


class SaveManager:
    def __init__(self):
        self.filepath = "prod/save.pkl"
        pathlib.Path(os.path.dirname(self.filepath)).mkdir(parents=True, exist_ok=True)
        if not os.path.isfile(self.filepath):
            open(self.filepath, "w").close()
        self.save_data = None

    def save(self):
        with open(self.filepath, "wb") as save_file:
            pickle.dump(self.save_data, save_file, pickle.HIGHEST_PROTOCOL)

    def load(self):
        with open(self.filepath, "rb") as save_file:
            self.save_data = pickle.load(save_file)

    def create_player_save(self, name):
        player = PlayerSaveData(name, [])
        self.save_data.player_data.append(player)
        self.save()
        return player

    def delete_player_save(self, player_save_data):
        self.save_data.player_data.remove(player_save_data)
        self.save()

    def can_create_file(self):
        return len(self.save_data.player_data) < 3
