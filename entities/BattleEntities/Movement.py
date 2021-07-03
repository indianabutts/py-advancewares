from entities.BattleMap.Map import Terrain


class MovementType:
    def __init__(self, name, terrain_movement_costs):
        self.name = name
        self.terrain_movement_costs = terrain_movement_costs

    def check_movement_possible(self, target_tile):
        return target_tile.terrain_type in self.terrain_movement_costs

    def move(self):
        pass

class WalkingMovement(MovementType):
    def __init__(self):
        terrain_movement_costs = {
            Terrain.GRASS:1,
            Terrain.ROAD:1
        }
        super().__init__("Walking", terrain_movement_costs)
