from enum import IntEnum
import threading
import pygame

class Alignment(IntEnum):
    Left = 0,
    Center = 1,
    Right = 2

class Message:
    """
        Represents a graphic message with a title and subtitle that can be drawn on a screen
    """

    def __init__(self, text_title = "", pos=(0,0)):

        self.text_title = text_title;
        self.pos = pos;

        self.text_subtitle= "";
        self.color_subtitle = (255, 255, 255);
        self.color_title = (255, 255, 255);
        self.text_title_size = 25;
        self.text_subtitle_size = 20;
        self.space_between_titles = 50;
        self.horizontal_alignment = Alignment.Center;
        self.title_font_name = "";
        self.subtitle_font_name = "";
        self.visible = False;
        self.timer = None;
        self.padding = 10;
        self.border_color = (255, 255, 255);
        self.background_color = (255, 255, 255);
        self.border_thickness = -1;
        self.queued_message = None;
        self.queued_message_time = 0;


    def draw(self, window):

        if(self.visible == False):
            return;

        font_title = pygame.font.SysFont(self.title_font_name, size=self.text_title_size);
        img_text_title = font_title.render(self.text_title, True, (self.color_title));

        img_text_title_size = img_text_title.get_size();

        font_subtitle = pygame.font.SysFont(self.subtitle_font_name, size=self.text_subtitle_size);
        img_text_subtitle = font_subtitle.render(self.text_subtitle, True, (self.color_subtitle));

        img_text_subtitle_size = img_text_subtitle.get_size();


        message_size = self.get_size();

        img_text_title_y = self.pos[1]+self.padding;
        img_text_subtitle_y = self.pos[1]+img_text_title_size[1]+self.space_between_titles+self.padding;


        if(self.horizontal_alignment == Alignment.Left):
            img_text_title_x = self.pos[0]+self.padding;
            img_text_subtitle_x = self.pos[0]+self.padding;

            message_rect = (self.pos[0], self.pos[1], message_size[0], message_size[1]);

        elif(self.horizontal_alignment == Alignment.Center):
            img_text_title_x = self.pos[0]-img_text_title_size[0]/2;
            img_text_subtitle_x = self.pos[0]-img_text_subtitle_size[0]/2;

            message_rect = (self.pos[0]-message_size[0]/2, self.pos[1], message_size[0], message_size[1]);

        elif(self.horizontal_alignment == Alignment.Right):
            img_text_title_x = self.pos[0]-message_size[0]+self.padding;
            img_text_subtitle_x = self.pos[0]-message_size[0]+self.padding;

            message_rect_x = self.pos[0]-message_size[0]-self.padding*2;
            message_rect = (message_rect_x, self.pos[1], message_size[0], message_size[1]);


        pygame.draw.rect(window, self.background_color, message_rect, 0);
        pygame.draw.rect(window, self.border_color, message_rect, self.border_thickness);

        window.blit(img_text_title, (img_text_title_x, img_text_title_y));
        window.blit(img_text_subtitle, (img_text_subtitle_x, img_text_subtitle_y));




    def show(self, time=None):

        self.visible = True;

        if(time != None):
            self.timer = threading.Timer(time, self.hide);
            self.timer.start();

    def hide(self):
        self.visible = False;

        if(self.queued_message != None):
            self.queued_message.show(self.queued_message_time);
            self.queued_message = None;


    def get_size(self):

        font_title = pygame.font.SysFont(self.title_font_name, size=self.text_title_size);
        img_text_title = font_title.render(self.text_title, True, (self.color_title));

        img_text_title_size = img_text_title.get_size();

        font_subtitle = pygame.font.SysFont(self.subtitle_font_name, size=self.text_subtitle_size);
        img_text_subtitle = font_subtitle.render(self.text_subtitle, True, (self.color_subtitle));

        img_text_subtitle_size = img_text_subtitle.get_size();

        if(img_text_subtitle_size[0] >= img_text_title_size[0]):
            max_width = img_text_subtitle_size[0];
        else:
            max_width = img_text_title_size[0];

        height = img_text_title_size[1]+self.padding*2;
        if(self.text_subtitle != ""):
            height += self.space_between_titles+img_text_subtitle_size[1];

        max_width += self.padding*2;

        return (max_width, height);

    def add_queued_message(self, message, time):
        self.queued_message = message;
        self.queued_message_time = time;



    #GETTERS/SETTERS
    def get_text_title(self):
        return self.text_title;

    def get_pos(self):
        return self.pos;

    def get_text_subtitle(self):
        return self.text_subtitle;

    def get_color_subtitle(self):
        return self.color_subtitle;

    def get_color_title(self):
        return self.color_title;

    def get_text_title_size(self):
        return self.text_title_size;

    def get_text_subtitle_size(self):
        return self.text_subtitle_size;

    def get_space_between_titles(self):
        return self.space_between_titles;

    def get_horizontal_alignment(self):
        return self.horizontal_alignment;

    def get_title_font_name(self):
        return self.title_font_name;

    def get_subtitle_font_name(self):
        return self.subtitle_font_name;

    def is_visible(self):
        return self.visible;

    def set_text_title(self, text_title):
        self.text_title = text_title;

    def set_pos(self, pos):
        self.pos = pos;

    def set_text_subtitle(self, text_subtitle):
        self.text_subtitle = text_subtitle;

    def set_color_subtitle(self, color_subtitle):
        self.color_subtitle = color_subtitle;

    def set_color_title(self, color_title):
        self.color_title = color_title;

    def set_text_title_size(self, text_title_size):
        self.text_title_size = text_title_size;

    def set_text_subtitle_size(self, text_subtitle_size):
        self.text_subtitle_size = text_subtitle_size;

    def set_space_between_titles(self, space_between_titles):
        self.space_between_titles = space_between_titles;

    def set_horizontal_alignment(self, horizontal_alignment):
        self.horizontal_alignment = horizontal_alignment;

    def set_title_font_name(self, title_font_name):
        self.title_font_name = title_font_name;

    def set_subtitle_font_name(self, subtitle_font_name):
        self.subtitle_font_name = subtitle_font_name;

    def set_visible(self, visible):
        self.visible = visible;

    def set_border_color(self, color):
        self.border_color = color;

    def set_background_color(self, color):
        self.background_color = color;

    def set_padding(self, padding):
        self.padding = padding;

    def set_border_thickness(self, thickness):
        self.border_thickness = thickness;