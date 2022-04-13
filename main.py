import pygame
from controller import Controller

pygame.init()
controller = Controller()
controller.create_interface()
controller.start_loop()


