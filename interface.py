from enum import Enum
from select import select
from grid import Grid, GRID_SIZE, save_grid_to_file, load_grid_from_file
from color import *
import pygame
import pycryptosat
from pathlib import Path
from button_widget import Button
from text_switch_widget import TextSwitchWidget
from message import Message, Alignment
import cnf
import webbrowser
import time

GRID_POS_X = 280
GRID_POS_Y = 50

class Interface:

    l_button = []
    l_menu_button = []
    l_tsw = []
    l_msg = []
    window_width=895
    window_height=670
    menu_width = 300
    menu_height = 300

    menu_displayed = False
    
    l_cell_selected = []
    select_mode = False
    remove_mode = False
    next_area_id = 0

    resolution_time = 0.000001

    def __init__(self, controller):
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('Dosun fuwari')

        self.controller = controller
        self.grid = Grid(GRID_POS_X, GRID_POS_Y)

        self.menu_x = self.window_width/2 - self.menu_width/2
        self.menu_y = self.window_height/2 - self.menu_height/2

        self.create_buttons()
        self.create_tsw()
        self.create_messages()

        self.load_images()

    #On crée tous les boutons et leur ajoute leurs caractéristiques pour avoir simplement à les dessiner ensuite
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
        self.bttn_apply.set_pos((105, 200))
        self.bttn_apply.set_padding(10)
        self.bttn_apply.set_text_size(24)
        self.bttn_apply.set_border(True)
        self.bttn_apply.set_border_color((0, 224, 73))
        self.bttn_apply.set_border_thickness(3)

        self.bttn_reset = Button("Réinitialiser")
        self.bttn_reset.set_color(BLACK)
        self.bttn_reset.set_background_color(WHITE)
        self.bttn_reset.set_pos((105, 250))
        self.bttn_reset.set_padding(10)
        self.bttn_reset.set_text_size(24)
        self.bttn_reset.set_border(True)
        self.bttn_reset.set_border_color((0, 224, 73))
        self.bttn_reset.set_border_thickness(3)

        self.bttn_random = Button("Grille aléatoire")
        self.bttn_random.set_color(BLACK)
        self.bttn_random.set_background_color(WHITE)
        self.bttn_random.set_pos((105, 315))
        self.bttn_random.set_padding(10)
        self.bttn_random.set_text_size(24)
        self.bttn_random.set_border(True)
        self.bttn_random.set_border_color((0, 224, 73))
        self.bttn_random.set_border_thickness(3)

        self.bttn_create_area = Button("Créer la région")
        self.bttn_create_area.set_color(BLACK)
        self.bttn_create_area.set_background_color(WHITE)
        self.bttn_create_area.set_padding(10)
        self.bttn_create_area.set_text_size(24)
        self.bttn_create_area.set_border(True)
        self.bttn_create_area.set_border_color((0, 224, 73))
        self.bttn_create_area.set_border_thickness(3)

        self.l_button.append(self.bttn_resolve)
        self.l_button.append(self.bttn_reset)
        self.l_button.append(self.bttn_random)
        self.l_button.append(self.bttn_apply)
        self.l_button.append(self.bttn_create_area)


        #Boutons du menu

        self.bttn_save_grid = Button("Sauvegarder la grille")
        self.bttn_save_grid.set_color(BLACK)
        self.bttn_save_grid.set_background_color(WHITE)
        self.bttn_save_grid.set_padding(10)
        self.bttn_save_grid.set_text_size(24)
        self.bttn_save_grid.set_border(True)
        self.bttn_save_grid.set_border_color((0, 224, 73))
        self.bttn_save_grid.set_border_thickness(3)

        self.bttn_load_grid = Button("Charger une grille")
        self.bttn_load_grid.set_color(BLACK)
        self.bttn_load_grid.set_background_color(WHITE)
        self.bttn_load_grid.set_padding(10)
        self.bttn_load_grid.set_text_size(24)
        self.bttn_load_grid.set_border(True)
        self.bttn_load_grid.set_border_color((0, 224, 73))
        self.bttn_load_grid.set_border_thickness(3)

        bttn_save_grid_x = self.menu_x + self.menu_width/2
        bttn_save_grid_y = self.menu_y + 150
        self.bttn_save_grid.set_pos((bttn_save_grid_x, bttn_save_grid_y))

        bttn_load_grid_x = self.menu_x + self.menu_width/2
        bttn_load_grid_y = self.menu_y + 200
        self.bttn_load_grid.set_pos((bttn_load_grid_x, bttn_load_grid_y))

        #On met les boutons du menu dans une autre liste pour pouvoir traiter les évênements et les dessiner seulement quand le menu est ouvert
        self.l_menu_button.append(self.bttn_save_grid)
        self.l_menu_button.append(self.bttn_load_grid)

    def create_tsw(self):
        
        self.tsw_grid_size = TextSwitchWidget()
        self.tsw_grid_size.set_pos(105, 140)
        self.tsw_grid_size.set_text_size(30)

        self.tsw_solver_choice = TextSwitchWidget()
        self.tsw_solver_choice.set_pos(105, 380)
        self.tsw_solver_choice.set_text_size(26)
        self.tsw_solver_choice.set_l_value(["Solveur maison", "Pycryptosat"])

        l_value = []
        for i in range(4, 31):
            l_value.append(str(i))

        self.tsw_grid_size.set_l_value(l_value)

        self.l_tsw.append(self.tsw_grid_size)
        self.l_tsw.append(self.tsw_solver_choice)

    def create_messages(self):

        self.message_bad_selection = Message()
        self.message_insat = Message()
        self.message_grid_saved = Message()
        self.message_grid_loaded = Message()

        self.l_msg.append(self.message_bad_selection)
        self.l_msg.append(self.message_insat)
        self.l_msg.append(self.message_grid_saved)
        self.l_msg.append(self.message_grid_loaded)

    #Charge les images et applique des traitements dessus
    def load_images(self):

        self.image_info = pygame.image.load(str(Path("Images/info.png")))
        self.image_info.convert()
        self.image_info = pygame.transform.smoothscale(self.image_info, (25, 25))

        self.image_open_menu = pygame.image.load(str(Path("Images/reglage.png")))
        self.image_open_menu.convert()
        self.image_open_menu = pygame.transform.smoothscale(self.image_open_menu, (30, 30))

        self.image_close_menu = pygame.image.load(str(Path("Images/cross.png")))
        self.image_close_menu.convert()
        self.image_close_menu = pygame.transform.smoothscale(self.image_close_menu, (20, 20))


    #Traite les évênements de la fenêtre
    def event(self, e):
        
        #Gestion des évênements du menu, s'il est ouvert
        if(e.type == pygame.MOUSEBUTTONUP and self.menu_displayed):

            mouse_x = e.pos[0]
            mouse_y = e.pos[1]

            #On ferme le menu si l'utilisateur a cliqué sur la croix
            image_close_menu_x = self.menu_x + self.menu_width - self.image_close_menu.get_size()[0]/2 - 20
            image_close_menu_y = self.menu_y + 20 - self.image_close_menu.get_size()[1]/2

            if mouse_x >= image_close_menu_x and mouse_x <= image_close_menu_x + self.image_close_menu.get_width():
                if mouse_y >= image_close_menu_y and mouse_y <= image_close_menu_y + self.image_close_menu.get_height():
                    self.menu_displayed = False

            for bttn in self.l_menu_button:

                if bttn.in_bounds(mouse_x, mouse_y):

                    if(bttn.get_text() == "Sauvegarder la grille"):
                        filepath = save_grid_to_file(self.grid)
                        self.menu_displayed = False
                        self.show_message_grid_saved(filepath)

                    elif(bttn.get_text() == "Charger une grille"):

                        grid_object = load_grid_from_file()
                        if(grid_object != None):
                            self.grid = grid_object

                        self.menu_displayed = False
                        self.show_message_grid_loaded()



        #Si le menu est ouvert on évite de traiter les évênements sur le reste de la fenêtre
        if(self.menu_displayed):
            return


        if(e.type == pygame.MOUSEBUTTONUP):

            mouse_x = e.pos[0]
            mouse_y = e.pos[1]

            #On regarde si l'utilisateur a cliqué sur la roue dentée permettant d'ouvrir le menu
            image_open_menu_x = 25 - self.image_open_menu.get_width()/2
            image_open_menu_y = 25 - self.image_open_menu.get_height()/2

            if mouse_x >= image_open_menu_x and mouse_x <= image_open_menu_x + self.image_open_menu.get_width():
                if mouse_y >= image_open_menu_y and mouse_y <= image_open_menu_y + self.image_open_menu.get_height():
                    self.menu_displayed = True

            #On regarde si l'utilisateur a cliqué sur l'image en haut à droite permettant d'ouvrir une page web expliquant les règles du Dosun Fuwari
            image_info_x = self.window_width-25-self.image_info.get_width()/2
            image_info_y = 25-self.image_info.get_height()/2

            if mouse_x >= image_info_x and mouse_x <= image_info_x + self.image_info.get_width():
                if mouse_y >= image_info_y and mouse_y <= image_info_y + self.image_info.get_height():
                    webbrowser.open('http://www.cross-plus-a.com/fr/html/cros7dsfw.htm', new=2)

            #On regarde si l'utilisateur a cliqué sur un des deux flèches permettant de changer la chaine de caractère sélectionnée , et on traite si c'est le cas
            for tsw in self.l_tsw:

                if(tsw.in_arrow_left_bounds(mouse_x, mouse_y)):
                    tsw.previous()
                elif(tsw.in_arrow_right_bounds(mouse_x, mouse_y)):
                    tsw.next()

            #On regarde si l'utilisateur a cliqué sur un des boutons de l'interface, hors menu, et on traite si c'est le cas
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
                        self.solve_grid()

                    elif(bttn.get_text() == "Grille aléatoire"):
                        self.grid.create_random_grid()
                                
                    
            if(e.button == 1):      #L'utilisateur a fait un click gauche ?
                if(self.select_mode):
                    print(self.grid.is_cell_seq_linked(self.l_cell_selected))
                self.select_mode=False

            elif(e.button == 2):    #L'utilisateur a fait un click molette  ?

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

            if(e.button == 1):   #L'utilisateur a fait un click gauche ?
                if(self.grid.is_in_grid(mouse_x, mouse_y)):

                    self.select_mode = True

                    cell = self.grid.get_cell_pos_from_pixel_coords(mouse_x, mouse_y,self.grid.get_n_case_x())
                    if cell not in self.l_cell_selected:
                        self.l_cell_selected.append(cell)
                        cell.set_is_selected(True)

            elif(e.button == 3):    #L'utilisateur a fait un click droit ?
                if(self.grid.is_in_grid(mouse_x, mouse_y)):

                    self.remove_mode = True

                    cell = self.grid.get_cell_pos_from_pixel_coords(mouse_x, mouse_y,self.grid.get_n_case_x())
                    if cell in self.l_cell_selected:
                        self.l_cell_selected.remove(cell)
                        cell.set_is_selected(False)

        elif(e.type == pygame.MOUSEMOTION):

            mouse_x = e.pos[0]
            mouse_y = e.pos[1]

            #Si l'utilisateur a gardé le click gauche appuyé et qu'il bouge sur la grille, on sélectionne les cases traversées
            if(self.grid.is_in_grid(mouse_x, mouse_y) and self.select_mode == True):

                cell = self.grid.get_cell_pos_from_pixel_coords(mouse_x, mouse_y,self.grid.get_n_case_x())
                if cell not in self.l_cell_selected:
                    self.l_cell_selected.append(cell)
                    cell.set_is_selected(True)

            #Si l'utilisateur a gardé le click droit appuyé et qu'il bouge sur la grille, on dé-sélectionne les cases traversées
            elif(self.grid.is_in_grid(mouse_x, mouse_y) and self.remove_mode == True):

                cell = self.grid.get_cell_pos_from_pixel_coords(mouse_x, mouse_y,self.grid.get_n_case_y())
                if cell in self.l_cell_selected:
                    self.l_cell_selected.remove(cell)
                    cell.set_is_selected(False)


    #On dessines sur la fenêtre
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

        self.window.blit(self.image_info, (self.window_width-25-self.image_info.get_width()/2, 25-self.image_info.get_height()/2))
        self.window.blit(self.image_open_menu, (25 - self.image_open_menu.get_width()/2, 25 - self.image_open_menu.get_height()/2))

        cell_size = GRID_SIZE/self.grid.get_n_case_x()
        for ball_case_pos in self.grid.get_l_ball_pos():

            ball_x = GRID_POS_X + ball_case_pos[0] * cell_size + cell_size/2
            ball_y = GRID_POS_Y + ball_case_pos[1] * cell_size + cell_size/2

            pygame.draw.circle(self.window, BLACK, (ball_x, ball_y), cell_size/4, width=2)

        for marble_case_pos in self.grid.get_l_marble_pos():

            marble_x = GRID_POS_X + marble_case_pos[0] * cell_size + cell_size/2
            marble_y = GRID_POS_Y + marble_case_pos[1] * cell_size + cell_size/2

            pygame.draw.circle(self.window, BLACK, (marble_x, marble_y), cell_size/4)

        #On dessine le texte affichant le temps de résolution
        font = pygame.font.SysFont(str(Path("Fonts/Roboto-Medium.ttf")), size=27)

        text_resolution_time = ""
        s = format(self.resolution_time, 'f').split(".")
        text_resolution_time += s[0]
        text_resolution_time += ","
        text_resolution_time += s[1][:6]
        text_resolution_time += " secs"

        text_resolution_time = font.render(text_resolution_time, True, WHITE)
        text_x = 80 - text.get_width()/2
        text_y = 24 - text.get_height()/2

        self.window.blit(text_resolution_time, (text_x, text_y))

        #On dessine les boutons sur la fenêtre
        for button in self.l_button:

            #On affiche le bouton "Créer la région" seulement si l'utilisateur a sélectionné une région
            if button.get_text() == "Créer la région":
                if len(self.l_cell_selected) != 0:
                    button.draw(self.window)
            else:
                button.draw(self.window)

        #On dessine les objets graphiques permettant de choisir une chaine de caractère à l'aide de 2 flèches 
        for tsw in self.l_tsw:
            tsw.draw(self.window)

        #On dessines les messages à destination de l'utilisateur
        for msg in self.l_msg:
            if msg.is_visible():
                msg.draw(self.window)

        #On dessine le menu si l'utilisateur l'a ouvert
        if(self.menu_displayed):
            self.draw_menu()

        #On actualise la fenêtre avec tout ce qu'on a dessiné précédemment
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

    #Dessine le menu sur la fenêtre. Il peut être ouvert en cliquant sur la roue dentée en haut à gauche de l'écran
    def draw_menu(self):
        
        menu_rect = (self.menu_x, self.menu_y, self.menu_width, self.menu_height)

        #On dessine les bordures et le fond du menu
        pygame.draw.rect(self.window, WHITE, menu_rect)
        pygame.draw.rect(self.window, BLACK, menu_rect, width=3)

        font = pygame.font.Font(str(Path("Fonts/Roboto-Medium.ttf")), 28)
        text_menu_title = font.render("Menu", True, BLACK)
        text_x = self.menu_x + self.menu_width/2 - text_menu_title.get_size()[0]/2
        text_y = self.menu_y + 20

        self.window.blit(text_menu_title, (text_x, text_y))

        #On dessine la croix pour que l'utilisateur puisse fermer le menu
        image_close_menu_x = self.menu_x + self.menu_width - self.image_close_menu.get_size()[0]/2 - 20
        image_close_menu_y = self.menu_y + 20 - self.image_close_menu.get_size()[1]/2

        self.window.blit(self.image_close_menu, (image_close_menu_x, image_close_menu_y))

        #On dessine les boutons du menus
        for bttn in self.l_menu_button:
            bttn.draw(self.window)


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
        self.bttn_create_area.set_pos((GRID_POS_X + 30, GRID_POS_Y + GRID_SIZE + 40))

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

    def show_message_grid_saved(self, file_path):

        title_text = "La grille a bien été sauvegardée !"

        self.message_grid_saved.set_text_title(title_text);
        self.message_grid_saved.set_text_subtitle("Chemin du fichier : " + file_path);
        self.message_grid_saved.set_horizontal_alignment(Alignment.Center);
        self.message_grid_saved.set_text_title_size(40);
        self.message_grid_saved.set_text_subtitle_size(25);
        self.message_grid_saved.set_space_between_titles(20);
        self.message_grid_saved.set_color_title((0, 0, 0));
        self.message_grid_saved.set_color_subtitle((0, 0, 0));
        self.message_grid_saved.set_border_color((0, 0, 0));
        self.message_grid_saved.set_border_thickness(4);
        self.message_grid_saved.set_title_font_name(str(Path("Fonts/Roboto-Medium.ttf")))

        self.message_grid_saved.set_pos((self.window_width/2, self.window_height/2-150))

        self.message_grid_saved.show(3)

    def show_message_grid_loaded(self):

        title_text = "La grille a été chargée avec succès !"

        self.message_grid_loaded.set_text_title(title_text);
        self.message_grid_loaded.set_horizontal_alignment(Alignment.Center);
        self.message_grid_loaded.set_text_title_size(40);
        self.message_grid_loaded.set_color_title((0, 0, 0));
        self.message_grid_loaded.set_border_color((0, 0, 0));
        self.message_grid_loaded.set_border_thickness(4);
        self.message_grid_loaded.set_title_font_name(str(Path("Fonts/Roboto-Medium.ttf")))

        self.message_grid_loaded.set_pos((self.window_width/2, self.window_height/2-150))

        self.message_grid_loaded.show(3)

    

    def solve_grid(self):

        if(self.grid.is_empty()):
            return

        cnf_ = cnf.convert_grid_to_cnf(self.grid)

        name_file = "file"
        cnf_.write_to_dimacs_file(name_file,self.grid.get_n_case_x(),self.grid.get_n_case_y())

        name_file_2 = name_file + "_3_sat"
        cnf_3sat = cnf.convert_cnf_to_3sat(cnf_,self.grid)
        cnf_3sat.write_to_dimacs_file(name_file_2,self.grid.get_n_case_x(),self.grid.get_n_case_y())


        start = time.monotonic()
        if(self.tsw_solver_choice.get_displayed_value() == "Solveur maison"):

            assignations=[]
            for i in range(1,self.grid.get_n_case_x()**2*2+1):
                assignations.append((i,False))
            sat,sol = cnf.dpll(cnf_,assignations)

        elif(self.tsw_solver_choice.get_displayed_value() == "Pycryptosat"):
            solver = pycryptosat.Solver()
            cnf_.add_clauses_to_pycryptosat_solver(solver)
            sat, sol = solver.solve()

        end = time.monotonic()
        self.resolution_time = end - start
        print(self.resolution_time)

        if sat == False :
            self.show_message_insat()
        else :
            #notre solver
            if(self.tsw_solver_choice.get_displayed_value() == "Solveur maison"):
                sol.sort()
                """
                for num, s in sol:
                    c = 
                    l =
                """
                for l in range(self.grid.get_n_case_x()):
                    for c in range(self.grid.get_n_case_x()):
                        cell = self.grid[l][c]
                        if cell.get_type() == 0:
                        
                            b = l*self.grid.get_n_case_x()+c+1
                            n = (l*self.grid.get_n_case_x()+c+1)+ self.grid.get_n_case_x()**2
                            numb,sb=sol[b-1]
                            num,sn=sol[n-1]
                            if sb :
                                self.grid.get_l_ball_pos().append((c, l))
                            if sn :
                                self.grid.get_l_marble_pos().append((c, l)) 

            elif(self.tsw_solver_choice.get_displayed_value() == "Pycryptosat"):             

                for l in range(self.grid.get_n_case_x()):
                    for c in range(self.grid.get_n_case_x()):
                        cell = self.grid[l][c]
                        if cell.get_type() == 0: 
                                            
                            b = l*self.grid.get_n_case_x()+c+1
                            n = (l*self.grid.get_n_case_x()+c+1)+ self.grid.get_n_case_x()**2
                            print(b, n)
                            if(sol[b] == True):
                                self.grid.get_l_ball_pos().append((c, l))
                            elif(sol[n] == True):
                                self.grid.get_l_marble_pos().append((c, l))


            
    def get_filepath_from_popup(self):

        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename()

        return file_path

