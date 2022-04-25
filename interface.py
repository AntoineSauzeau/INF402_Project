from enum import Enum
from select import select
from grid import Grid, GRID_SIZE
from color import *
import pygame
import pycryptosat
from pathlib import Path
from button_widget import Button
from text_switch_widget import TextSwitchWidget
from message import Message, Alignment
import cnf

GRID_POS_X = 280
GRID_POS_Y = 50

class Interface:

    l_button = []
    l_tsw = []
    l_msg = []
    window_width=675
    window_height=450
    
    l_cell_selected = []
    select_mode = False
    remove_mode = False
    next_area_id = 0

    def __init__(self, controller):
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('Dosun fuwari')

        self.controller = controller
        self.grid = Grid(GRID_POS_X, GRID_POS_Y)

        self.create_buttons()
        self.create_tsw()
        self.create_messages()

    def create_buttons(self):

        self.bttn_resolve = Button("Résoudre")
        self.bttn_resolve.set_color(BLACK)
        self.bttn_resolve.set_background_color(WHITE)
        self.bttn_resolve.set_pos((GRID_POS_X + GRID_SIZE, GRID_POS_Y + GRID_SIZE + 40))
        self.bttn_resolve.set_padding(10)
        self.bttn_resolve.set_text_size(24)
        self.bttn_resolve.set_border(True)
        self.bttn_resolve.set_border_color((0, 224, 73))
        self.bttn_resolve.set_border_thickness(3)

        self.bttn_apply = Button("Appliquer")
        self.bttn_apply.set_color(BLACK)
        self.bttn_apply.set_background_color(WHITE)
        self.bttn_apply.set_pos((100, 200))
        self.bttn_apply.set_padding(10)
        self.bttn_apply.set_text_size(24)
        self.bttn_apply.set_border(True)
        self.bttn_apply.set_border_color((0, 224, 73))
        self.bttn_apply.set_border_thickness(3)

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

        self.create_area = Button("Créer la région")
        self.create_area.set_color(BLACK)
        self.create_area.set_background_color(WHITE)
        self.create_area.set_padding(10)
        self.create_area.set_text_size(24)
        self.create_area.set_border(True)
        self.create_area.set_border_color((0, 224, 73))
        self.create_area.set_border_thickness(3)

        self.l_button.append(self.bttn_resolve)
        self.l_button.append(self.bttn_reset)
        self.l_button.append(self.bttn_random)
        self.l_button.append(self.bttn_apply)
        self.l_button.append(self.create_area)

    def create_tsw(self):
        
        self.tsw_grid_size = TextSwitchWidget()
        self.tsw_grid_size.set_pos(100, 140)
        self.tsw_grid_size.set_text_size(16)

        l_value = []
        for i in range(4, 31):
            l_value.append(str(i))

        self.tsw_grid_size.set_l_value(l_value)

        self.l_tsw.append(self.tsw_grid_size)

    def create_messages(self):

        self.message_bad_selection = Message()
        self.message_insat = Message()

        self.l_msg.append(self.message_bad_selection)
        self.l_msg.append(self.message_insat)


    def event(self, e):
        
        if(e.type == pygame.MOUSEBUTTONUP):

            mouse_x = e.pos[0]
            mouse_y = e.pos[1]

            for tsw in self.l_tsw:

                if(tsw.in_arrow_left_bounds(mouse_x, mouse_y)):
                    tsw.previous()
                elif(tsw.in_arrow_right_bounds(mouse_x, mouse_y)):
                    tsw.next()

            for bttn in self.l_button:

                if bttn.in_bounds(mouse_x, mouse_y):
                
                    if(bttn.get_text() == "Appliquer"):
                        self.grid.set_n_case_x(int(self.tsw_grid_size.get_displayed_value()))
                        self.grid.set_n_case_y(int(self.tsw_grid_size.get_displayed_value()))

                    elif(bttn.get_text() == "Créer la région"):

                        #On vérifie que la région sélectionné est bien contigue
                        if(self.grid.is_cell_seq_linked(self.l_cell_selected) == False):
                            self.show_message_bad_selection()

                            for cell in self.l_cell_selected:
                                cell.set_is_selected(False)

                        else:
                            for cell in self.l_cell_selected:
                                cell.set_area(self.next_area_id)
                                cell.set_is_selected(False)

                            self.next_area_id += 1

                        self.l_cell_selected.clear()

                    elif(bttn.get_text() == "Réinitialiser"):
                        self.grid.reset()
                        self.l_cell_selected.clear()

                        self.grid.get_l_ball_pos().clear()
                        self.grid.get_l_marble_pos().clear()

                    elif(bttn.get_text() == "Résoudre"):
                        solver = pycryptosat.Solver()
                        cnf_ = cnf.convert_grid_to_cnf(self.grid)
                        name_file = "file"
                        cnf_.write_to_dimacs_file(name_file,self.grid.get_n_case_x(),self.grid.get_n_case_y(), solver)
                        cnf2 = cnf.convert_cnf_to_3sat(cnf_,self.grid)
                        name2 = name_file + "_3_sat"
                        cnf2.write_to_dimacs_file(name2,self.grid.get_n_case_x(),self.grid.get_n_case_y(), solver)
                        sat, sol = solver.solve()
                        if sat == False :
                            self.show_message_insat()
                        else :
                            for l in range(self.grid.get_n_case_x()):
                                for c in range(self.grid.get_n_case_x()):
                                    cell = self.grid[l][c]
                                    if cell.get_type() == 0:
    
                                        
                                        b = l*self.grid.get_n_case_x()+c+1
                                        n = (l*self.grid.get_n_case_x()+c+1)+ self.grid.get_n_case_x()**2
                                        if(sol[b] == True):
                                            self.grid.get_l_ball_pos().append((c, l))
                                        elif(sol[n] == True):
                                            self.grid.get_l_marble_pos().append((c, l))

                                        
                                
                                
                    
            if(e.button == 1):
                if(self.select_mode):
                    print(self.grid.is_cell_seq_linked(self.l_cell_selected))
                self.select_mode=False

            elif(e.button == 2):

                cell = self.grid.get_cell_pos_from_pixel_coords(mouse_x, mouse_y,self.grid.get_n_case_x())
                if(cell.get_type() == 0):
                    cell.set_type(1)
                else:
                    cell.set_type(0)

                cell.set_area(-1)
                print(cell.get_type())

            elif(e.button == 3):
                self.remove_mode=False
                
        elif(e.type == pygame.MOUSEBUTTONDOWN):
            
            mouse_x = e.pos[0]
            mouse_y = e.pos[1]

            if(e.button == 1 or e.button == 3):
                if(self.grid.is_in_grid(mouse_x, mouse_y)):
                    self.message_bad_selection.hide()

            if(e.button == 1):   #Left click
                if(self.grid.is_in_grid(mouse_x, mouse_y)):

                    self.select_mode = True

                    cell = self.grid.get_cell_pos_from_pixel_coords(mouse_x, mouse_y,self.grid.get_n_case_x() )
                    self.l_cell_selected.append(cell)
                    cell.set_is_selected(True)

            elif(e.button == 3):    #Right click
                if(self.grid.is_in_grid(mouse_x, mouse_y)):

                    self.remove_mode = True

                    cell = self.grid.get_cell_pos_from_pixel_coords(mouse_x, mouse_y,self.grid.get_n_case_x())
                    if cell in self.l_cell_selected:
                        self.l_cell_selected.remove(cell)
                        cell.set_is_selected(False)

        elif(e.type == pygame.MOUSEMOTION):

            mouse_x = e.pos[0]
            mouse_y = e.pos[1]

            if(self.grid.is_in_grid(mouse_x, mouse_y) and self.select_mode == True):

                cell = self.grid.get_cell_pos_from_pixel_coords(mouse_x, mouse_y,self.grid.get_n_case_x())
                if cell not in self.l_cell_selected:
                    self.l_cell_selected.append(cell)
                    cell.set_is_selected(True)

            elif(self.grid.is_in_grid(mouse_x, mouse_y) and self.remove_mode == True):

                cell = self.grid.get_cell_pos_from_pixel_coords(mouse_x, mouse_y,self.grid.get_n_case_y())
                if cell in self.l_cell_selected:
                    self.l_cell_selected.remove(cell)
                    cell.set_is_selected(False)



    def draw(self):

        if(self.get_size()[0] != self.window_width or self.get_size()[1] != self.window_height):
            (self.window_width, self.window_height) = self.get_size()
            self.update_window_size()

        self.update_widget_pos()
        
        background_rect = (0, 0, self.window_width, self.window_height)
        pygame.draw.rect(self.window, (46, 40, 42), background_rect)

        for l in range(self.grid.get_n_case_y()):
            for c in range(self.grid.get_n_case_x()):

                if(self.grid[l][c].get_type() == 0):
                    cell_color = WHITE
                elif(self.grid[l][c].get_type() == 1):
                    cell_color = GREY_2

                if(self.grid[l][c].get_is_selected() == True):
                    cell_color = RED
                
                cell_x = GRID_POS_X + c * (GRID_SIZE/self.grid.get_n_case_x())
                cell_y = GRID_POS_Y + l * (GRID_SIZE/self.grid.get_n_case_x())

                rect_cell = (cell_x, cell_y, (GRID_SIZE/self.grid.get_n_case_x()), (GRID_SIZE/self.grid.get_n_case_x()))
                pygame.draw.rect(self.window, cell_color, rect_cell)
                
                self.draw_cell_borders(self.grid[l][c], rect_cell)


        pygame.draw.line(self.window, WHITE, (210, 0), (210, self.window_height))

        font = pygame.font.SysFont(str(Path("Fonts/Roboto-Medium.ttf")), size=20)

        for i in range(self.grid.get_n_case_x()):

            text = font.render(str(i+1), True, WHITE)
            text_x = GRID_POS_X + (GRID_SIZE/self.grid.get_n_case_x())/2 - text.get_width()/2 + i * (GRID_SIZE/self.grid.get_n_case_x())
            text_y = GRID_POS_Y - 12 - text.get_height()/2
 
            self.window.blit(text, (text_x, text_y))

        for i in range(self.grid.get_n_case_y()):

            text = font.render(str(i+1), True, WHITE)
            text_x = GRID_POS_X - 12 - text.get_width()/2
            text_y = GRID_POS_Y + (GRID_SIZE/self.grid.get_n_case_x())/2 - text.get_height()/2 + i * (GRID_SIZE/self.grid.get_n_case_x())
 
            self.window.blit(text, (text_x, text_y))

        font = pygame.font.SysFont(str(Path("Fonts/Roboto-Medium.ttf")), size=35)

        text_title = font.render("Dosum fuwari", True, WHITE)
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

        cell_size = GRID_SIZE/self.grid.get_n_case_x()
        for ball_case_pos in self.grid.get_l_ball_pos():

            ball_x = GRID_POS_X + ball_case_pos[0] * cell_size + cell_size/2
            ball_y = GRID_POS_Y + ball_case_pos[1] * cell_size + cell_size/2

            pygame.draw.circle(self.window, BLACK, (ball_x, ball_y), cell_size/4, width=2)

        for marble_case_pos in self.grid.get_l_marble_pos():

            marble_x = GRID_POS_X + marble_case_pos[0] * cell_size + cell_size/2
            marble_y = GRID_POS_Y + marble_case_pos[1] * cell_size + cell_size/2

            pygame.draw.circle(self.window, BLACK, (marble_x, marble_y), cell_size/4)

        for button in self.l_button:

            if button.get_text() == "Créer la région":
                if len(self.l_cell_selected) != 0:
                    button.draw(self.window)
            else:
                button.draw(self.window)

        for tsw in self.l_tsw:
            tsw.draw(self.window)

        for msg in self.l_msg:
            if msg.is_visible():
                msg.draw(self.window)

        pygame.display.flip()

    def draw_cell_borders(self, cell, rect_cell):

        if(cell.get_area() == -1 and cell.get_type() == 0):
            border_rect = (rect_cell[0], rect_cell[1], (GRID_SIZE/self.grid.get_n_case_x())-1, (GRID_SIZE/self.grid.get_n_case_x())-1)
            pygame.draw.rect(self.window, BLUE, rect_cell, width=2)
        else:
            c_top = self.grid.get_top_cell(cell)
            c_bottom = self.grid.get_bottom_cell(cell)
            c_left = self.grid.get_left_cell(cell)
            c_right = self.grid.get_right_cell(cell)
 
            if(c_top == None or c_top.get_area() != cell.get_area() or cell.get_type() == 1):
                top_border_rect = (rect_cell[0], rect_cell[1], (GRID_SIZE/self.grid.get_n_case_x()), 3)
                pygame.draw.rect(self.window, BLACK, top_border_rect, width=0)
            else:
                top_border_rect = (rect_cell[0], rect_cell[1], (GRID_SIZE/self.grid.get_n_case_x()), 1)
                pygame.draw.rect(self.window, GREY, top_border_rect, width=0)

            if(c_bottom == None or c_bottom.get_area() != cell.get_area() or cell.get_type() == 1):
                bottom_border_rect = (rect_cell[0], rect_cell[1] + (GRID_SIZE/self.grid.get_n_case_x()) - 2, (GRID_SIZE/self.grid.get_n_case_x()), 2)
                pygame.draw.rect(self.window, BLACK, bottom_border_rect, width=0)
            else:
                bottom_border_rect = (rect_cell[0], rect_cell[1] + (GRID_SIZE/self.grid.get_n_case_x()) - 1, (GRID_SIZE/self.grid.get_n_case_x()), 1)
                pygame.draw.rect(self.window, GREY, bottom_border_rect, width=0)

            if(c_left == None or c_left.get_area() != cell.get_area() or cell.get_type() == 1):
                left_border_rect = (rect_cell[0], rect_cell[1], 2, (GRID_SIZE/self.grid.get_n_case_x()))
                pygame.draw.rect(self.window, BLACK, left_border_rect, width=0)
            else:
                left_border_rect = (rect_cell[0], rect_cell[1], 1, (GRID_SIZE/self.grid.get_n_case_x()))
                pygame.draw.rect(self.window, GREY, left_border_rect, width=0)

            if(c_right == None or c_right.get_area() != cell.get_area() or cell.get_type() == 1):
                right_border_rect = (rect_cell[0] + (GRID_SIZE/self.grid.get_n_case_x()) - 2, rect_cell[1], 2, (GRID_SIZE/self.grid.get_n_case_x()))
                pygame.draw.rect(self.window, BLACK, right_border_rect, width=0)
            else:
                right_border_rect = (rect_cell[0] + (GRID_SIZE/self.grid.get_n_case_x()) - 1, rect_cell[1], 1, (GRID_SIZE/self.grid.get_n_case_x()))
                pygame.draw.rect(self.window, GREY, right_border_rect, width=0)

    def get_size(self):

        frame_1_width = 210
        frame_2_width = 70 + GRID_SIZE + 75

        width = frame_1_width + frame_2_width
        height = 50 + GRID_SIZE + 80

        return (width, height)

    def update_window_size(self):
        self.window = pygame.display.set_mode((self.get_size()[0], self.get_size()[1]))

    def update_widget_pos(self):
        self.bttn_resolve.set_pos((GRID_POS_X + GRID_SIZE, GRID_POS_Y + GRID_SIZE + 40))
        self.create_area.set_pos((GRID_POS_X + 30, GRID_POS_Y + GRID_SIZE + 40))

        self.bttn_reset.set_pos((100, self.window_height - 40))
        self.bttn_random.set_pos((100, self.window_height - 90))

    def show_message_bad_selection(self):

        title_text = "Attention : La région doit être contigue"

        self.message_bad_selection.set_text_title(title_text)
        self.message_bad_selection.set_horizontal_alignment(Alignment.Center)
        self.message_bad_selection.set_text_title_size(26)
        self.message_bad_selection.set_color_title(RED)
        self.message_bad_selection.set_background_color(GREY)
        self.message_bad_selection.set_title_font_name(str(Path("Fonts/Roboto-Medium.ttf")))

        self.message_bad_selection.set_pos((GRID_POS_X + 195, GRID_POS_Y + GRID_SIZE + 20))

        self.message_bad_selection.show(10)

    def show_message_insat(self):

        title_text = "Cette grille est insatisfiable"

        self.message_insat.set_text_title(title_text)
        self.message_insat.set_horizontal_alignment(Alignment.Center)
        self.message_insat.set_text_title_size(26)
        self.message_insat.set_color_title(RED)
        self.message_insat.set_background_color(GREY)
        self.message_insat.set_title_font_name(str(Path("Fonts/Roboto-Medium.ttf")))

        self.message_insat.set_pos((GRID_POS_X + 195, GRID_POS_Y + GRID_SIZE + 20))

        self.message_insat.show(10)

