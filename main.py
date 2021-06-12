import sys

import pygame
from pygame.locals import *
from core.SokobanGame import SokobanGame

if __name__ == "__main__":
    sokoban_game = SokobanGame()
    sokoban_game.run_game()
