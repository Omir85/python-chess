import pygame
from ui import create_window

def test_create_window_defaults():
    window = create_window()
    assert window.get_width() == 500
    assert window.get_height() == 500
    assert pygame.display.get_caption()[0] == "title"
    
def test_create_window():
    window = create_window(200, 300, "test new window")
    assert window.get_width() == 200
    assert window.get_height() == 300
    assert pygame.display.get_caption()[0] == "test new window"