from time import sleep

import cv2 as cv2
import numpy as np

from src.model.Case import Case
from src.controller.MouseEvent import get_next_click_mouse

from PIL import Image, ImageGrab

from ahk import AHK


class Plateau:
    def __init__(self, ahk: AHK):
        self.ahk = ahk

        # get position premier dé en haut à gauche
        x_1, y_1, _, _ = get_next_click_mouse()

        sleep(0.5)
        # get position dernier dé en bas à droite
        x_2, y_2, _, _ = get_next_click_mouse()

        width_dice = int((x_2 - x_1)/4)
        height_dice = int((y_2 - y_1)/2)

        self.cases = [[Case(j*width_dice + x_1, i*height_dice + y_1, width_dice, height_dice) for j in range(5)] for i in range(3)]

        self.screen_size = (1920, 1080)

    def scan(self):
        """Met à jours les dés présents"""
        image = grab_image(box=(0, 0, self.screen_size[0], self.screen_size[1]))
        for case_row in self.cases:
            for case in case_row:
                print(case.get_average_color(image))


def pil_to_cv2(image_pil):
    return cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)


def grab_image(box=(0, 0, 1920, 1080)):
    width = box[2] - box[0]
    height = box[3] - box[1]
    return pil_to_cv2(ImageGrab.grab(bbox=box))
