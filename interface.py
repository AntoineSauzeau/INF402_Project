from enum import Enum
import pygame
import sys

class Page(Enum):
    GridParam = 0
    Main = 1

PAGE_GRID_PARAM_WIDTH=800
PAGE_GRID_PARAM_HEIGHT=500

class Interface:

    def __init__(self, controller):
        self.window = pygame.display.set_mode((500, 500))

        self.page = Page.GridParam
        self.controller = controller

    def event(self, event):

        if(self.page == Page.GridParam):
            self.event_page_grid_param()
        elif(self.page == Page.Main):
            self.event_page_main()

    def draw(self):
        
        if(self.page == Page.GridParam):
            self.draw_page_grid_param()
        elif(self.page == Page.Main):
            self.draw_page_main()

        pygame.display.flip()

    def event_page_grid_param(self):
        pass

    def event_page_main(self):
        pass

    def draw_page_grid_param(self):
        
        background_rect = (0, 0, PAGE_GRID_PARAM_WIDTH, PAGE_GRID_PARAM_HEIGHT)
        pygame.draw.rect(self.window, (46, 40, 42), background_rect)

    def draw_page_main(self):
        pass


