from os import listdir
from os.path import isfile

from entities.Player import Player
from entities.Tile import *

vec = pygame.Vector2


class LevelManager:
    def __init__(self, level_number):
        folder_path = os.path.join("assets", "level_data")
        self.level_files = sorted(
            [
                f
                for f in listdir(folder_path)
                if isfile(os.path.join(folder_path, f)) and "boxxle" in f
            ],
            key=lambda x: int(x.partition("_")[2].partition(".")[0]),
        )
        self.level_number = level_number
        self.current_level = self.get_level_by_number(level_number)
        self.player = Player(self.current_level.player_start)

    def get_level_by_number(self, level_number):
        self.level_number = level_number - 1
        return self._filename_to_level(self.level_files[self.level_number])

    def get_next_level(self):
        self.level_number += 1
        return self._filename_to_level(self.level_files[self.level_number])

    def _filename_to_level(self, filename):
        level_name = filename.split(".")[0]
        self.current_level = Level(level_name)
        return self.current_level


class Level:
    def __init__(self, level_name):
        self.filename = os.path.join("assets", "level_data", level_name + ".txt")
        print("Loading Level " + self.filename)
        self.tiles = []
        self.grid = {}
        self.player_start = pygame.Vector2(0, 0)
        self.level_number = 0
        self.level_group = 0
        self.level_sub_number = 0
        self.box_count = 0
        self.goal_count = 0
        self.boxes_on_goal_count = 0
        self.level_name = ""
        self.size = pygame.Vector2(0, 0)
        self.brick_locations = []
        self.parse_level_file()
        self.flood_fill()
        self.level_surface = pygame.Surface(self.size * 16)

    def parse_level_file(self):
        self.goal_count = 0
        self.boxes_on_goal_count = 0
        self.box_count = 0
        with open(self.filename, "r") as level_file:
            line = level_file.readline()
            count = 1
            while line:
                if count == 1:
                    self.level_number = int(line)
                if count == 2:
                    self.level_name = line
                if count == 3:
                    dimensions = line.split(",")
                    self.size = pygame.Vector2(int(dimensions[0]), int(dimensions[1]))
                #            if line == "-":
                if count > 4:
                    y = count - 5
                    x = 0
                    for character in line:
                        current_grid_location = pygame.Vector2(x, y)
                        if character == "#":
                            brick = Brick(current_grid_location)
                            self.tiles.append(brick)
                            self.brick_locations.append(current_grid_location)
                            self._add_to_grid(current_grid_location, brick)
                        if character == "G":
                            goal = Goal(current_grid_location)
                            self.tiles.append(goal)
                            self._add_to_grid(current_grid_location, goal)
                            self.goal_count += 1
                        if character == "B":
                            box = Box(current_grid_location)
                            self.tiles.append(box)
                            self._add_to_grid(current_grid_location, box)
                            self.box_count += 1
                        if character == "Z":
                            box = Box(current_grid_location)
                            goal = Goal(current_grid_location)
                            self.tiles.append(box)
                            self.tiles.append(goal)
                            self._add_to_grid(current_grid_location, box)
                            self._add_to_grid(current_grid_location, goal)
                            self.box_count += 1
                            self.goal_count += 1
                        if character == "P":
                            self.player_start = current_grid_location
                        x += 1

                line = level_file.readline()
                count += 1
                self.level_group = int(self.level_number / 5) + 1
                self.level_sub_number = self.level_number % 6
                self.update_box_on_goal_count()

    def reset_level(self):
        for tile in self.tiles:
            tile.set_position(tile.start_position)
        self.update_box_on_goal_count()

    def flood_fill(self):
        checked_locations = []
        locations_to_check = [self.player_start]
        while len(locations_to_check) > 0:
            current_location = locations_to_check.pop()
            location_key = self._vec2_to_key(current_location)
            north = current_location + pygame.Vector2(0, -1)
            south = current_location + pygame.Vector2(0, 1)
            west = current_location + pygame.Vector2(-1, 0)
            east = current_location + pygame.Vector2(1, 0)
            checked_locations.append(current_location)
            if north not in self.brick_locations:
                if north not in checked_locations:
                    locations_to_check.append(north)
            if east not in self.brick_locations:
                if east not in checked_locations:
                    locations_to_check.append(east)
            if south not in self.brick_locations:
                if south not in checked_locations:
                    locations_to_check.append(south)
            if west not in self.brick_locations:
                if west not in checked_locations:
                    locations_to_check.append(west)

            if current_location not in self.brick_locations:
                floor = Floor(current_location)
                self.tiles.append(floor)
                self._add_to_grid(current_location, floor)

    def _vec2_to_key(self, vector):
        return "{},{}".format(vector.x, vector.y)

    def _add_to_grid(self, location, tile):
        location_key = self._vec2_to_key(location)
        if location_key not in self.grid:
            self.grid[location_key] = []
        self.grid[location_key].append(tile)

    def get_tiles(self):
        return sorted(self.tiles, key=lambda x: x.priority)

    def check_target_location(self, grid_location):
        matching_tiles = []
        for tile in self.tiles:
            if tile.grid_position == grid_location:
                matching_tiles.append(tile)
        return matching_tiles

    def update_box_on_goal_count(self):
        box_locations = []
        goal_locations = []
        box_dictionary = {}
        box_on_goal_count = 0
        for tile in self.tiles:
            if isinstance(tile, Box):
                box_locations.append(tile.grid_position)
                location_key = self._vec2_to_key(tile.grid_position)
                tile.set_standard_sprite()
                if location_key not in box_dictionary:
                    box_dictionary[location_key] = {}
                box_dictionary[location_key] = tile
            if isinstance(tile, Goal):
                goal_locations.append(tile.grid_position)
        for goal in goal_locations:
            if goal in box_locations:
                box_dictionary[self._vec2_to_key(goal)].set_on_goal_sprite()
                box_on_goal_count += 1
        self.boxes_on_goal_count = box_on_goal_count
