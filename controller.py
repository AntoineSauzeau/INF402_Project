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
        """
            Start the event/display loop
        """

        clock = pygame.time.Clock();
        while(not(self.exit)):

            try:
                for event in pygame.event.get():

                    self.interface.event(event);

                self.interface.draw();

            #If the user wants to close the program with Ctrl-C, we close him
            except KeyboardInterrupt:
                self.quit();


            except Exception as err:
                print(err)
                sys.exit(-1)


            clock.tick(self.FPS);



    def create_interface(self):
        self.interface = Interface(self);

    def quit(self):

        print("Fin du programme.");
        self.exit = True;