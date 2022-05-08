from interface import Interface
import pygame
from pygame.locals import *
import time
import threading
import sys


class Controller():
    """
        Manages the event/display loop, the pygame interface and catches fatal errors
    """

    FPS = 160;

    def __init__(self):

        print("Constructor Controller");

        self.exit = False;


    def start_loop(self):

        #    Start the event/display loop


        clock = pygame.time.Clock();
        while(not(self.exit)):

            try:
                for event in pygame.event.get():

                    if event.type == pygame.QUIT:
                        self.quit();

                    self.interface.event(event);

                self.interface.draw();

            #Si l'utilisateur veut fermer le programme avec Ctrl+C : ok
            except KeyboardInterrupt:
                self.quit();

            clock.tick(self.FPS);



    def create_interface(self):
        self.interface = Interface(self);

    def quit(self):

        print("Fin du programme.");
        self.exit = True;