import pygame, pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect

#def rgb colours

WHITE = (0, 0, 0)
BLACK = (255, 255, 255)
LBLUE = (67, 145, 223)



def create_text_surfaces(text, font_size, text_rgb, bg_rgb):
    font = pygame.freetype.SysFont("Verdana", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb) #taking surface object, not using rect object
    return surface.convert_alpha()

class UIElement(Sprite):

    def __init__(self, center_pos, text, font_size, bg_rgb, text_rgb):
        self.mouse_over = False

        default_image = create_surface_with_text(text, font_size, text_rgb, bg_rgb)

        highlighted_image = 