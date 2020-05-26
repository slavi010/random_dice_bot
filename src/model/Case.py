import cv2 as cv2
import numpy as np

from src.model.DiceEnum import DiceColorEnum
from src.model.Utils import same_color, same_color_offset_rgb


class Case:
    def __init__(self, x: int, y: int, width: int, height: int):
        if x < 0 or y < 0:
            raise Exception("x or y cant be <0")
        if width <= 0 or height <= 0:
            raise Exception("width or height cant be <0")

        self.x = x
        self.y = y

        # with and height af a dice
        self.width = width
        self.height = height

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

        avg_color_per_row = np.average(
            img[box[1]:box[3], box[0]:box[2]],
            axis=0,
        )
        avg_color = np.average(avg_color_per_row, axis=0)
        return avg_color

    def is_joker_dice(self, image):
        color = image[self.y + int(self.height*10/50)][self.x]
        # print('joker color : ' + str(color))
        return same_color_offset_rgb(color, (150, 232, 216), offset_rgb=(50, 15, 30))

    def get_dot_dice(self, image, is_joker: bool):
        #
        # *   * (0     1)
        # * * * (2  3  4)
        # *   * (5     6)
        #
        x_offset = int(self.width / 5)
        y_offset = int(self.height / 5)
        dots_color = [image[coord[1]][coord[0]] for coord in self.coord_all_dots()]

        # 1*
        tmp_dots = dots_color.copy()
        tmp_dots.pop(3)
        if not is_dots(tmp_dots, is_joker):
            return 1, dots_color[3]

        # 2*
        tmp_dots = dots_color.copy()
        tmp_dots.pop(1)
        tmp_dots.pop(5)
        if is_dots(tmp_dots, is_joker):
            return 2, dots_color[1]

        # 3*
        tmp_dots = dots_color.copy()
        tmp_dots.pop(1)
        tmp_dots.pop(3 - 1)
        tmp_dots.pop(5 - 2)
        if not is_dots(tmp_dots, is_joker):
            return 3, dots_color[3]

        # 4*
        tmp_dots = dots_color.copy()
        tmp_dots.pop(0)
        tmp_dots.pop(1 - 1)
        tmp_dots.pop(5 - 2)
        tmp_dots.pop(6 - 3)
        if not is_dots(tmp_dots, is_joker):
            return 4, dots_color[1]

        # 5*
        tmp_dots = dots_color.copy()
        tmp_dots.pop(0)
        tmp_dots.pop(1 - 1)
        tmp_dots.pop(3 - 2)
        tmp_dots.pop(5 - 3)
        tmp_dots.pop(6 - 4)
        if not is_dots(tmp_dots, is_joker):
            return 5, dots_color[3]

        # TODO : 7

        return 6, dots_color[1]
    
    def coord_all_dots(self):
        x_offset = int(self.width / 5)
        y_offset = int(self.height / 5)
        return [(self.x - x_offset, self.y - y_offset),
                (self.x + x_offset, self.y - y_offset),
                (self.x - x_offset, self.y),
                (self.x, self.y),
                (self.x + x_offset, self.y),
                (self.x - x_offset, self.y + y_offset),
                (self.x + x_offset, self.y + y_offset)]

    def __str__(self):
        return '({0} {1}) {2}'.format(self.x, self.y, self.dice)


def is_dots(dots_color, is_joker: bool):
    for dot_idx in range(len(dots_color)):
        for name, member in DiceColorEnum.__members__.items():
            for color in member.value:
                if same_color(dots_color[dot_idx], color):
                    return True
        if is_joker:
            if not (dots_color[dot_idx][0] > 250 and dots_color[dot_idx][1] > 250 and dots_color[dot_idx][2] > 250):
                # pas blanc
                for j in range(dot_idx+1, len(dots_color)):
                    if same_color(dots_color[dot_idx], dots_color[j]):
                        return True
    return False
