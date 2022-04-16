import pygame
from controller import Controller
import sys

pygame.init()

try:
    controller = Controller()
    controller.create_interface()
    controller.start_loop()
except Exception as e:
    exception_type, exception_object, exception_traceback = sys.exc_info()
    filename = exception_traceback.tb_frame.f_code.co_filename
    line_number = exception_traceback.tb_lineno

    print("Exception type: ", exception_type)
    print("File name: ", filename)
    print("Line number: ", line_number)
    print(e)


