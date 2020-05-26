import cv2 as cv2
import numpy as np


class Case:
    def __init__(self, x: int, y: int, width: int, height: int):
        if x < 0 or y < 0:
            raise Exception("x or y cant be <0")
        if width <= 0 or height <= 0:
            raise Exception("width or height cant be <0")

        self.x = x
        self.y = y

        # with and height af a dice
        self.width = 50
        self.height = 50

        self.dice = None

    def get_box_coord(self):
        """:return x1, y1, x2, y2"""
        return int(self.x - self.width / 2), \
               int(self.y - self.height / 2), \
               int(self.x + self.width / 2), \
               int(self.y + self.height / 2)

    def get_average_color(self, img):
        """Get the average color of the dice.

        :return r, g, b"""
        box = self.get_box_coord()

        avg_color_per_row = np.average(img[box[1]:box[3], box[0]:box[2]], axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)
        return avg_color

    def __str__(self):
        return '({0} {1}) {2}'.format(self.x, self.y, self.dice)
