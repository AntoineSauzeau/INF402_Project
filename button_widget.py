import pygame

class Button():
    """
        Implements a graphic button that can be drawn on a pygame surface
    """

    def __init__(self, text="", font="", pos=(0,0), text_size=20, color=(255, 255, 255)):
        pygame.sprite.Sprite.__init__(self);

        self.text = text;
        self.font_name = font;
        self.pos = pos;
        self.text_size = text_size;
        self.color = color;

        self.highlighted = False;
        self.underline = False;
        self.border = False;
        self.border_color = (255, 255, 255);
        self.padding = 0
        self.border_thickness = 1
        self.background_color = None;

    def draw(self, window):
        """
            Draw the button on the window or on a pygame surface
        """

        if(self.highlighted):
            color = self.h_color;
            text_size = self.h_text_size;
        else:
            color = self.color;
            text_size = self.text_size;

        font = pygame.font.SysFont(self.font_name, size=text_size);
        font.set_underline(self.underline);

        text_image = font.render(self.text, True, color);

        size = self.get_size();

        if(self.background_color != None):
            border_rect = (self.pos[0]-size[0]/2, self.pos[1]-size[1]/2, size[0], size[1]);
            window.fill(self.background_color, border_rect);

        draw_pos = (self.pos[0]-size[0]/2+self.padding, self.pos[1]-size[1]/2+self.padding);
        window.blit(text_image, draw_pos);

        if(self.border):
            border_rect = (self.pos[0]-size[0]/2, self.pos[1]-size[1]/2, size[0], size[1]);
            pygame.draw.rect(window, self.border_color, border_rect, self.border_thickness);



    def highlight(self, scale, color):
        """
            Highlights the button, i.e. enlarges it or changes its colour from its basic state
        """

        self.highlighted = True;
        if(color != None):
            self.h_color = color;
        else:
            self.h_color = self.color;

        self.h_scale = scale
        self.h_text_size = int(self.text_size+self.text_size*scale);

    def remove_highlighting(self):
        self.highlighted = False;

    def in_bounds(self, x, y):
        """
            Returns True if the coordinates are within the frame of the button, returns False if not
        """

        size = self.get_size();

        xmin = self.pos[0] - size[0]/2;
        xmax = self.pos[0] + size[0]/2;

        ymin = self.pos[1] - size[1]/2;
        ymax = self.pos[1] + size[1]/2;

        return (x >= xmin and x <= xmax and y >= ymin and y <= ymax);

    def get_size(self):
        """
            Returns the size of the button
        """

        if(self.highlighted):
            text_size = self.h_text_size;
        else:
            text_size = self.text_size;

        font = pygame.font.SysFont(self.font_name, size=text_size);
        font.set_underline(self.underline);

        img_text_size = font.size(self.text);
        button_size = (img_text_size[0]+self.padding*2, img_text_size[1]+self.padding*2);

        return button_size;



    #SETTERS/GETTERS
    def set_text(self, text):
        self.text = text;

    def set_font(self, font_name):
        self.font_name = font_name;

    def set_text_size(self, text_size):
        self.text_size = text_size;

    def set_color(self, color):
        self.color = color;

    def set_pos(self, pos):
        self.pos = pos;

    def get_text(self):
        return self.text;

    def set_underline(self, underline):
        self.underline = underline;

    def set_border(self, border):
        self.border = border;

    def set_border_color(self, color):
        self.border_color = color

    def set_padding(self, padding):
        self.padding = padding;

    def set_border_thickness(self, thickness):
        self.border_thickness = thickness;

    def set_background_color(self, background_color):
        self.background_color = background_color;