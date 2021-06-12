import os
import math
import pygame

NUMBER_FONTSET = pygame.image.load(os.path.join("assets", "number_font.png"))
TEXT_FONTSET = pygame.image.load(os.path.join("assets", "text_font.png"))

vec = pygame.Vector2


class LevelDisplay:
    def __init__(self, digits, major_value, minor_value):
        self.number_split = int(digits / 2)
        self.surf = pygame.Surface((8 * ((self.number_split * 2) + 3), 8))
        self.number_display_major = NumberDisplay(self.number_split, major_value)
        self.number_display_minor = NumberDisplay(self.number_split, minor_value)
        self.prefix = {
            "rect": pygame.Rect((10 * 8, 0, 16, 8)),
            "image": pygame.Surface(pygame.Rect((10 * 8, 0, 16, 8)).size).convert(),
            "position": (0, 0),
        }
        self.hyphen = {
            "rect": pygame.Rect((12 * 8, 0, 8, 8)),
            "image": pygame.Surface(pygame.Rect((12 * 8, 0, 8, 8)).size).convert(),
            "position": (self.number_split, 0),
        }

        self.prefix["image"].blit(NUMBER_FONTSET.convert(), (0, 0), self.prefix["rect"])
        self.hyphen["image"].blit(NUMBER_FONTSET.convert(), (0, 0), self.hyphen["rect"])
        self.surf.blit(self.prefix["image"], (0, 0))
        self.surf.blit(self.number_display_major.surf, (2 * 8, 0))
        self.surf.blit(self.hyphen["image"], ((2 + self.number_split) * 8, 0))
        self.surf.blit(self.number_display_minor.surf, ((3 + self.number_split) * 8, 0))

    def set_value(self, major_value, minor_value):
        self.number_display_major.set_value(major_value)
        self.number_display_minor.set_value(minor_value)
        self.surf.blit(self.number_display_major.surf, (2 * 8, 0))
        self.surf.blit(self.number_display_minor.surf, ((3 + self.number_split) * 8, 0))


class NumberDisplay:
    def __init__(self, digits, starting_value=0):
        super().__init__()
        self.surf = pygame.Surface((8 * digits, 8))
        self.value_string = starting_value.__str__().rjust(digits, "0")
        self.surf.fill((0, 0, 0))
        self.digits = []
        index = 0
        for digit in self.value_string:
            self.digits.append(Number(int(digit), index))
            self.surf.blit(self.digits[index].image, (index * 8, 0))
            index += 1

    def set_value(self, value):
        self.value_string = value.__str__().rjust(len(self.digits), "0")
        index = 0
        for digit in self.digits:
            digit.set_value(int(self.value_string[index]))
            self.surf.blit(self.digits[index].image, (index * 8, 0))
            index += 1


class Number(pygame.sprite.Sprite):
    def __init__(self, value, position):
        super().__init__()
        self.surf = pygame.Surface((8, 8))
        self.value = value
        self.position = position
        self.surf.fill((0, 0, 0))
        self.rect = pygame.Rect(value * 8, 0, 8, 8)
        self.image = pygame.Surface(self.rect.size).convert()
        self.image.blit(NUMBER_FONTSET.convert(), (0, 0), self.rect)

    def set_value(self, value):
        self.value = value
        self.rect = pygame.Rect(value * 8, 0, 8, 8)
        self.image = pygame.Surface(self.rect.size).convert()
        self.image.blit(NUMBER_FONTSET.convert(), (0, 0), self.rect)

    def __str__(self):
        return "[{}] {}".format(self.position, self.value)


PANEL_SHEET = pygame.image.load(os.path.join("assets", "panel.png"))


class UIPanel(pygame.sprite.Sprite):
    def __init__(self, size, screen_position=vec(0, 0)):
        self.size = size
        self.int_size = vec(int(size.x / 8), int(size.y / 8))
        self.surf = pygame.Surface((size.x, size.y))
        self.surf.fill((255, 255, 255))
        self.corner = {
            "rect": pygame.Rect(0, 0, 8, 8),
            "image": pygame.Surface((8, 8)).convert(),
        }
        self.edge = {
            "rect": pygame.Rect(8, 0, 8, 8),
            "image": pygame.Surface((8, 8)).convert(),
        }
        self.corner["image"].blit(PANEL_SHEET.convert(), (0, 0), self.corner["rect"])
        self.edge["image"].blit(PANEL_SHEET.convert(), (0, 0), self.edge["rect"])
        self.build_surfaces()
        self.screen_position = screen_position
        pass

    def render(self):
        self.surf.fill((255, 255, 255))
        self.build_surfaces()

    def get_top_position(self):
        return self.screen_position

    def get_bottom_position(self):
        return self.screen_position + vec(self.screen_position.x, self.size.y)

    def get_right_position(self):
        return self.screen_position + vec(self.size.x, self.screen_position.y)

    def get_left_position(self):
        return self.screen_position

    def get_size(self):
        return self.size

    def build_surfaces(self):
        for y in range(0, int(self.int_size.y)):
            for x in range(0, int(self.int_size.x)):
                if x == 0 and y == 0:
                    self.surf.blit(self.corner["image"], (x * 8, y * 8))
                if x == self.int_size.x - 1 and y == self.int_size.y - 1:
                    self.surf.blit(
                        pygame.transform.rotate(self.corner["image"], 180),
                        (x * 8, y * 8),
                    )
                if y == 0 and x != 0 and x != self.int_size.x - 1:
                    self.surf.blit(self.edge["image"], (x * 8, y * 8))
                if y == self.int_size.y - 1 and x != 0 and x != self.int_size.x - 1:
                    self.surf.blit(
                        pygame.transform.rotate(self.edge["image"], 180), (x * 8, y * 8)
                    )
                if x == 0 and y != 0 and y != self.int_size.y - 1:
                    self.surf.blit(
                        pygame.transform.rotate(self.edge["image"], 90), (x * 8, y * 8)
                    )
                if x == self.int_size.x - 1 and y != 0 and y != self.int_size.y - 1:
                    self.surf.blit(
                        pygame.transform.rotate(self.edge["image"], 270), (x * 8, y * 8)
                    )
                if x == self.int_size.x - 1 and y == 0:
                    self.surf.blit(
                        pygame.transform.rotate(self.corner["image"], 270),
                        (x * 8, y * 8),
                    )
                if x == 0 and y == self.int_size.y - 1:
                    self.surf.blit(
                        pygame.transform.rotate(self.corner["image"], 90),
                        (x * 8, y * 8),
                    )


class Text(pygame.sprite.Sprite):
    def __init__(self, text, position=0):
        self.text = text
        self.position = position
        self.lower_text = self.text.lower()
        self.surf = pygame.Surface((8 * len(self.text), 8))
        self.render()

    def _get_font_index(self, character):
        if character.isalpha():
            return ord(character) - 97
        if character == "!":
            return 26
        if character == "?":
            return 27
        if character == ">":
            return 28
        if character == "^":
            return 29
        if character == ".":
            return 30
        if character == "-":
            return 31

    def update_text(self, text):
        self.text = text
        self.lower_text = self.text.lower()
        self.render()

    def render(self):
        self.surf.fill((255, 255, 255))
        index = 0
        for character in self.lower_text:
            FONTSET = None
            character_offset = 0
            if character.isnumeric():
                FONTSET = NUMBER_FONTSET
                character_offset = int(character)
            else:
                FONTSET = TEXT_FONTSET
                character_offset = self._get_font_index(character)
            if character != " ":
                rect = pygame.Rect(character_offset * 8, 0, 8, 8)
                image = pygame.Surface(rect.size).convert()
                image.blit(FONTSET.convert(), (0, 0), rect)
                self.surf.blit(image, (index * 8, 0))
            index += 1


class TextUIOption(Text):
    def __init__(self, text, position, callback):
        super().__init__(text, position)
        self.callback = callback

    def select(self):
        return self.callback()

    def __str__(self):
        return "Option: {}".format(self.text)


class TextOptionsUIPanel(UIPanel):
    def __init__(
        self,
        size,
        options,
        header_text=None,
        default_option=0,
        screen_position=vec(0, 0),
    ):
        header_check = ""
        if header_text is not None:
            header_check = header_text
        final_size = vec(max(size.x, (len(header_check) + 2) * 8), size.y)
        super().__init__(final_size, screen_position)
        self.option_index = 0
        self.options = sorted(options, key=lambda x: x.position, reverse=False)
        self.current_option = self.options[self.option_index]
        self.hidden = True
        self.header_text = header_text
        self.header = None
        self.render()

    def next_option(self):
        self.option_index = (self.option_index + 1) % len(self.options)
        self.current_option = self.options[self.option_index]
        self.render()

    def previous_option(self):
        self.option_index = (self.option_index - 1) % len(self.options)
        self.current_option = self.options[self.option_index]
        self.render()

    def render(self):
        super().render()
        index = 0
        if self.header_text is not None:
            self.header = Text(self.header_text)
            self.surf.blit(self.header.surf, (8, 8))
            index += 2

        for option in self.options:
            if option == self.current_option:
                rect = pygame.Rect(28 * 8, 0, 8, 8)
                image = pygame.Surface(rect.size).convert()
                image.blit(TEXT_FONTSET.convert(), (0, 0), rect)
                self.surf.blit(image, (8, (index + 1) * 8))
            self.surf.blit(option.surf, (16, (index + 1) * 8))
            index += 1


class TextPanel(UIPanel):
    def __init__(self, text, size=vec(0, 0), screen_position=vec(0, 0)):
        size_x = max(size.x, (len(text) + 2) * 8)
        size_y = max(size.y, 24)
        super().__init__(vec(size_x, size_y), screen_position)
        self.textUI = Text(text, 0)
        self.render()

    def render(self):
        super().render()
        self.textUI.render()
        self.surf.blit(self.textUI.surf, (8, 8))

    def change_text(self, text):
        self.textUI.update_text(text)
        self.render()


class KeyboardUIPanel(UIPanel):
    def __init__(
        self,
        characters_per_row,
        finish_callback,
        character_limit=8,
        attached_text_panel=None,
        screen_position=vec(0, 0),
    ):
        size_x = (characters_per_row * 2 + 4) * 8
        size_y = (math.ceil(26 / characters_per_row) * 2 + 4) * 8
        self.rows = math.ceil(26 / characters_per_row)
        self.attached_text_panel = attached_text_panel
        self.character_limit = character_limit
        size = vec(size_x, size_y)
        super().__init__(size, screen_position)
        self.entered_text = ""
        self.characters_per_row = characters_per_row
        self.index = vec(0, 0)
        self.enter_callback = finish_callback
        self.characters = {}
        self.character_map = []
        self.selection_character = Text("^")
        x_list = []
        for i in range(0, 26):
            current_character = chr(97 + i)
            y = i // characters_per_row
            x = i % characters_per_row

            character = TextUIOption(current_character, i, self._character_callback)
            position = vec(x=x * 16 + 16, y=y * 16 + 16)
            self.characters[character] = position
            x_list.append(character)
            if x == characters_per_row - 1 or current_character == "z":
                self.character_map.append(x_list)
                x_list = []
        self.delete_option = TextUIOption(
            "DEL", len(self.character_map), self._delete_selected
        )
        self.enter_option = TextUIOption(
            "ENTER", len(self.character_map) + 1, self.enter_callback
        )
        self.characters[self.delete_option] = vec(
            x=16, y=self.characters[self.character_map[-1][-1]].y + 16
        )
        self.characters[self.enter_option] = vec(
            x=64, y=self.characters[self.character_map[-1][-1]].y + 16
        )
        self.character_map.append([self.delete_option, self.enter_option])
        self.current_character = self.character_map[int(self.index.y)][
            int(self.index.x)
        ]
        self.render()

    def _delete_selected(self):
        self.entered_text = self.entered_text[:-1]
        self.attached_text_panel.change_text(self.entered_text)

    def _character_callback(self):
        self.entered_text += self.current_character.text
        self.attached_text_panel.change_text(self.entered_text)

    def select(self):
        return self.current_character.callback()

    def move_up(self):
        self.index.y = (self.index.y - 1) % len(self.character_map)
        self.index.x = min(self.index.x, len(self.character_map[int(self.index.y)]) - 1)
        self.current_character = self.character_map[int(self.index.y)][
            int(self.index.x)
        ]

    def move_down(self):
        self.index.y = (self.index.y + 1) % len(self.character_map)
        self.index.x = min(self.index.x, len(self.character_map[int(self.index.y)]) - 1)
        self.current_character = self.character_map[int(self.index.y)][
            int(self.index.x)
        ]

    def move_left(self):
        self.index.x = (self.index.x - 1) % len(self.character_map[int(self.index.y)])
        self.current_character = self.character_map[int(self.index.y)][
            int(self.index.x)
        ]

    def move_right(self):
        self.index.x = (self.index.x + 1) % len(self.character_map[int(self.index.y)])
        self.current_character = self.character_map[int(self.index.y)][
            int(self.index.x)
        ]

    def render(self):
        super().render()

        for character, position in self.characters.items():
            self.surf.blit(character.surf, position)
        self.surf.blit(
            self.selection_character.surf,
            self.characters[self.current_character] - vec(0, 8),
        )


class MultiColumnOptionPanel(UIPanel):
    def __init__(self, size, options, columns, header_text=None, default_option=0):
        sizes = [size.x, (len(header_text) + 2) * 8]
        final_size = vec(max(size.x, (len(header_text) + 2) * 8), size.y)
        for option in options:
            (len(option.text) + 2) * 8
        super().__init__(final_size)
        self.option_index = 0
        self.options = sorted(options, key=lambda x: x.position, reverse=False)
        self.current_option = self.options[self.option_index]
        self.hidden = True
        self.header_text = header_text
        self.header = None
        self.render()


"""
MultiColumnOptionPanel goal is to create a panel that looks something like
 ------------------------ 
| Heading                |
|                        |
| >Option A    Something |
|  Option B    Something |
|  Option C    Something |
|                        |
|                        |
|________________________|
"""
