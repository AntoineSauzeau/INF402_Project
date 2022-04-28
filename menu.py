

from locale import setlocale
from sre_parse import WHITESPACE
from color import * 
import pygame

class Menu:

    def __init__(self, menu_name):
        
        self.menu_name = menu_name
        self.l_value = []
        self.menu_name_font = ""
        self.menu_name_size = 20
        self.value_size = 20
        self.value_font = ""
        self.background_color = WHITE
        self.border_color = BLACK
        self.text_color = BLACK
        self.x = 0
        self.y = 0
        self.padding_left = 10
        self.padding_right = 10
        self.padding_top = 10
        self.padding_bottom = 10

    def draw(self):
        pass

    def get_dim(self):

        max_width = 0
        height = 0
        for value in self.l_value:

            font = pygame.font.SysFont(self.value_font, size=self.value_size)
            text_image = font.render(value, True, self.color)

            cell_width = self.padding_left + text_image.get_width() + self.padding_right
            cell_height = self.padding_bottom + text_image.get_height() + self.padding_top
            max_width = max(cell_width, max_width)
            height = height + cell_height

        font = pygame.font.SysFont(self.menu_name_font, size=self.menu_name_size)
        text_image = font.render(self.text, True, self.color)

        cell_width = self.padding_left + text_image.get_width() + self.padding_right
        cell_height = self.padding_bottom + text_image.get_height() + self.padding_top
        max_width = max(cell_width, max_width)
        height = height + cell_height

        return (max_width, height)

    def get_height(self):
        pass