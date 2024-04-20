import pygame
import sys


def quit_event(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()