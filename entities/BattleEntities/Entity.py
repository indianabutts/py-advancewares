from core.Stats import Stat


class Entity:
    def __init__(self, name, grid_location, base_health, commander=None):
        self.name = name
        self.grid_location = grid_location
        self.base_health = Stat("Health", base_health)
        self.commander = commander

    def move_to_grid_location(self, target_grid_location):
        self.grid_location = target_grid_location


class Unit(Entity):
    def __init__(
        self,
        name,
        grid_location,
        base_health,
        base_movement_range,
        base_fuel,
        base_attack_range,
        attack_deadzone,
        movement_type,
        commander=None
    ):
        super().__init__(name, grid_location, base_health, commander)
        self.movement_range = Stat("Movement Range", base_movement_range)
        self.fuel = Stat("Fuel", base_fuel)
        self.attack_range = Stat("Attack Range", base_attack_range)
        self.deadzone = attack_deadzone
        self.movement_type = movement_type

    def attack(self, target):
        pass

    def capture(self, target):
        pass

    def __str__(self):
        return "{}".format(self.name)


class Building(Entity):
    def __init__(self, name, grid_location, base_health, commander=None):
        super().__init__(name, grid_location, base_health, commander)