import os
import pygame

class TextSwitchWidget:
    """
        Represents a widget allowing to choose a value from a string list using 2 arrows
    """

    def __init__(self, text_size=30, pos=(0,0), l_value=[]):

        self.text_size = text_size;
        self.l_value = l_value;
        self.pos = pos;

        self.index = 0;
        self.font_name = "";
        self.text_color = (255, 255, 255);

        self.img_arrow_right = pygame.image.load(os.path.join("Images", "right-arrow.png"));
        self.img_arrow_left = pygame.image.load(os.path.join("Images", "left-arrow.png"));


    def draw(self, window):

        if(len(self.l_value) == 0):
            return;

        text = self.l_value[self.index];

        font = pygame.font.SysFont(self.font_name, size=self.text_size);
        img_text = font.render(text, True, self.text_color);

        img_text_size = img_text.get_size();
        img_arrow_size = int(img_text_size[1]+img_text_size[1]/2)

        img_arrow_right = pygame.transform.scale(self.img_arrow_right, (img_arrow_size, img_arrow_size));
        img_arrow_left = pygame.transform.scale(self.img_arrow_left, (img_arrow_size, img_arrow_size));

        img_text_x = self.pos[0]-img_text_size[0]/2;
        img_text_y = self.pos[1]-img_text_size[1]/2;

        window.blit(img_text, (img_text_x, img_text_y));


        arrow_left_x = self.pos[0]-img_text_size[0]/2-17-img_arrow_size/2;
        arrow_left_y = self.pos[1]-img_arrow_size/2;

        arrow_right_x = self.pos[0]+img_text_size[0]/2+17-img_arrow_size/2;
        arrow_right_y = self.pos[1]-img_arrow_size/2;

        window.blit(img_arrow_left, (arrow_left_x, arrow_left_y));
        window.blit(img_arrow_right, (arrow_right_x, arrow_right_y));

    def next(self):

        if(self.index+1 != len(self.l_value)):
            self.index += 1;
        else:
            self.index = 0;

    def previous(self):

        if(self.index-1 != -1):
            self.index -= 1;
        else:
            self.index = len(self.l_value)-1;

    def in_arrow_left_bounds(self, x, y):

        if(self.index >= len(self.l_value)):
            return False;

        text = self.l_value[self.index];

        font = pygame.font.SysFont(self.font_name, size=self.text_size);
        img_text = font.render(text, True, self.text_color);

        img_text_size = img_text.get_size();
        img_arrow_size = int(img_text_size[1]+img_text_size[1]/2)

        arrow_left_x = self.pos[0]-img_text_size[0]/2-17-img_arrow_size/2;
        arrow_left_y = self.pos[1]-img_arrow_size/2;

        x_min = arrow_left_x;
        x_max = x_min + img_arrow_size;
        y_min = arrow_left_y;
        y_max = y_min + img_arrow_size;

        return (x_min <= x and x <= x_max and y_min <= y and y <= y_max);

    def in_arrow_right_bounds(self, x, y):

        if(self.index >= len(self.l_value)):
            return False;

        text = self.l_value[self.index];

        font = pygame.font.SysFont(self.font_name, size=self.text_size);
        img_text = font.render(text, True, self.text_color);

        img_text_size = img_text.get_size();
        img_arrow_size = int(img_text_size[1]+img_text_size[1]/2)

        arrow_right_x = self.pos[0]+img_text_size[0]/2+17-img_arrow_size/2;
        arrow_right_y = self.pos[1]-img_arrow_size/2;

        x_min = arrow_right_x;
        x_max = x_min + img_arrow_size;
        y_min = arrow_right_y;
        y_max = y_min + img_arrow_size;

        return (x_min <= x and x <= x_max and y_min <= y and y <= y_max);


    def get_size(self):
        pass;


    #GETTERS/SETTERS
    def set_text_size(self, text_size):
        self.text_size;

    def set_l_value(self, l_value):
        self.l_value = l_value;

    def set_pos(self, x, y):
        self.pos = (x, y);

    def set_font_name(self, font_name):
        self.font_name = font_name;

    def set_text_color(self, text_color):
        self.text_color = text_color;

    def set_index(self, index):
        self.index = index;

    def get_index(self):
        return self.index;

    def get_displayed_value(self):
        return self.l_value[self.index];