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