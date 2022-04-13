from enum import Enum
from grid import CELL_SIZE, Grid
from color import *
import pygame
from pathlib import Path
from button_widget import Button
from text_switch_widget import TextSwitchWidget

GRID_POS_X = 280
GRID_POS_Y = 50

class Interface:

    l_button = []
    l_tsw = []
    window_width=675
    window_height=450

    def __init__(self, controller):
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('Dosun fuwari')

        self.controller = controller
        self.grid = Grid(GRID_POS_X, GRID_POS_Y)

        self.create_buttons()
        self.create_tsw()

    def create_buttons(self):

        self.bttn_resolve = Button("Résoudre")
        self.bttn_resolve.set_color(BLACK)
        self.bttn_resolve.set_background_color(WHITE)
        self.bttn_resolve.set_pos((GRID_POS_X + self.grid.get_grid_width(), GRID_POS_Y + self.grid.get_grid_height() + 40))
        self.bttn_resolve.set_padding(10)
        self.bttn_resolve.set_text_size(24)
        self.bttn_resolve.set_border(True)
        self.bttn_resolve.set_border_color((0, 224, 73))
        self.bttn_resolve.set_border_thickness(3)

        self.bttn_reset = Button("Réinitialiser")
        self.bttn_reset.set_color(BLACK)
        self.bttn_reset.set_background_color(WHITE)
        self.bttn_reset.set_pos((100, 250))
        self.bttn_reset.set_padding(10)
        self.bttn_reset.set_text_size(24)
        self.bttn_reset.set_border(True)
        self.bttn_reset.set_border_color((0, 224, 73))
        self.bttn_reset.set_border_thickness(3)

        self.bttn_random = Button("Grille aléatoire")
        self.bttn_random.set_color(BLACK)
        self.bttn_random.set_background_color(WHITE)
        self.bttn_random.set_pos((100, 315))
        self.bttn_random.set_padding(10)
        self.bttn_random.set_text_size(24)
        self.bttn_random.set_border(True)
        self.bttn_random.set_border_color((0, 224, 73))
        self.bttn_random.set_border_thickness(3)

        self.l_button.append(self.bttn_resolve)
        self.l_button.append(self.bttn_reset)
        self.l_button.append(self.bttn_random)

    def create_tsw(self):
        
        self.tsw_grid_size = TextSwitchWidget()
        self.tsw_grid_size.set_pos(100, 140)
        self.tsw_grid_size.set_l_value(["0", "1", "2", "3"])
        self.tsw_grid_size.set_text_size(16)

        self.l_tsw.append(self.tsw_grid_size)


    def event(self, e):
        
        if(e.type == pygame.MOUSEBUTTONUP):

            mouse_x = e.pos[0]
            mouse_y = e.pos[1]

            for tsw in self.l_tsw:

                if(tsw.in_arrow_left_bounds(mouse_x, mouse_y)):
                    tsw.previous()
                elif(tsw.in_arrow_right_bounds(mouse_x, mouse_y)):
                    tsw.next()

    def draw(self):

        if(self.get_size()[0] != self.window_width or self.get_size()[1] != self.window_height):
            (self.window_width, self.window_height) = self.get_size()
            self.update_window_size()
        
        background_rect = (0, 0, self.window_width, self.window_height)
        pygame.draw.rect(self.window, (46, 40, 42), background_rect)

        for l in range(self.grid.get_n_case_y()):
            for c in range(self.grid.get_n_case_x()):

                if(self.grid[l][c].get_type() == 0):
                    cell_color = WHITE
                elif(self.grid[l][c].get_type() == 1):
                    cell_color = BLACK
                
                cell_x = GRID_POS_X + c * CELL_SIZE
                cell_y = GRID_POS_Y + l * CELL_SIZE

                rect_cell = (cell_x, cell_y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.window, cell_color, rect_cell)

                border_rect = (cell_x, cell_y, CELL_SIZE-1, CELL_SIZE-1)
                pygame.draw.rect(self.window, BLUE, rect_cell, width=1)


        pygame.draw.line(self.window, WHITE, (210, 0), (210, self.window_height))

        font = pygame.font.SysFont(str(Path("Fonts/Roboto-Medium.ttf")), size=20)

        for i in range(self.grid.get_n_case_x()):

            text = font.render(str(i), True, WHITE)
            text_x = GRID_POS_X + CELL_SIZE/2 - text.get_width()/2 + i * CELL_SIZE
            text_y = GRID_POS_Y - 12 - text.get_height()/2
 
            self.window.blit(text, (text_x, text_y))

        for i in range(self.grid.get_n_case_y()):

            text = font.render(str(i), True, WHITE)
            text_x = GRID_POS_X - 12 - text.get_width()/2
            text_y = GRID_POS_Y + CELL_SIZE/2 - text.get_height()/2 + i * CELL_SIZE
 
            self.window.blit(text, (text_x, text_y))

        font = pygame.font.SysFont(str(Path("Fonts/Roboto-Medium.ttf")), size=35)

        text_title = font.render("Dosum fuwaru", True, WHITE)
        text_x = 20 - text.get_width()/2
        text_y = 100 - text.get_height()/2
 
        #self.window.blit(text_title, (text_x, text_y))

        font = pygame.font.SysFont(str(Path("Fonts/Roboto-Medium.ttf")), size=33)

        text_grid_size = font.render("Taille de la grille", True, WHITE)
        text_x = 30 - text.get_width()/2
        text_y = 100 - text.get_height()/2
 
        self.window.blit(text_grid_size, (text_x, text_y))

        image_info = pygame.image.load(str(Path("Images/info.png")))
        image_info.convert()
        image_info = pygame.transform.smoothscale(image_info, (25, 25))
        self.window.blit(image_info, (self.window_width-25-image_info.get_width()/2, 25-image_info.get_height()/2))

        for button in self.l_button:
            button.draw(self.window)

        for tsw in self.l_tsw:
            tsw.draw(self.window)

        pygame.display.flip()

    def get_size(self):

        frame_1_width = 210
        frame_2_width = 70 + self.grid.get_grid_width() + 75

        width = frame_1_width + frame_2_width
        height = 50 + self.grid.get_grid_height() + 80

        return (width, height)

    def update_window_size(self):
        self.window = pygame.display.set_mode((self.get_size()[0], self.get_size()[1]))

