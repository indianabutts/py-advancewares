from enum import Enum


class ModifierType(Enum):
    ADDITIVE = 1
    PERCENTAGE = 2
    MULTIPLIER = 3


class Modifier:
    def __init__(self, target_stat_name, modifier_type, value, stackable=False):
        self.target_stat_name = target_stat_name
        self.modifier_type = modifier_type
        self.stackable = stackable
        self.value = value

    def modify_value(self, start_value):
        if self.modifier_type == ModifierType.ADDITIVE:
            return start_value + self.value
        if self.modifier_type == ModifierType.PERCENTAGE:
            return start_value * (1 + self.value)
        if self.modifier_type == ModifierType.MULTIPLIER:
            return start_value * self.value


class Stat:
    def __init__(self, name, base_value):
        self.name = name
        self.base_value = base_value
        self.current_value = base_value
        self._effective_value = base_value
        self.modifiers = []
        self.dirty_modifiers = False

    def add_modifier(self, modifier):
        if not modifier.stackable and modifier in self.modifiers:
            self.modifiers.remove(modifier)
        self.modifiers.append(modifier)
        self.dirty_modifiers = True

    def get_effective_value(self):
        if not self.dirty_modifiers:
            return self._effective_value
        self._effective_value = self.base_value
        for modifier in self.modifiers:
            self._effective_value = modifier.modify_value(self._effective_value)
        return self._effective_value


class Entity:
    def __init__(self, name, grid_location, base_health):
        self.name = name
        self.grid_location = grid_location
        self.base_health = Stat("Health", base_health)

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
    ):
        super().__init__(name, grid_location, base_health)
        self.movement_range = Stat("Movement Range", base_movement_range)
        self.fuel = Stat("Fuel", base_fuel)
        self.attack_range = Stat("Attack Range", base_attack_range)
        self.deadzone = attack_deadzone
        self.movement_type = "TODO"

    def __str__(self):
        return "{}".format(self.name)
