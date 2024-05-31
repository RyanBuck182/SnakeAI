import os
import pygame
from ui import main_menu


if __name__ == '__main__':
    os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'

    next_ui = main_menu
    while next_ui is not None:
        next_ui = next_ui()

    pygame.quit()
