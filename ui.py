import pygame

def create_window(width=500, height=500, window_title="title"):
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption(window_title)
    return window

if __name__ == "__main__":
    pass