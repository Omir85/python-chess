import pygame
import colors

def draw_text(surface, text, size, color, x, y):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)
    
    draw_label(surface, label, (x, y))

def draw_label(surface, label, coordinates):
    # print(surface)
    surface.blit(label, coordinates)

def clear_window(window, color = colors.BLACK_COLOR):
    window.fill(color)

def redraw_window():
    pygame.display.update()