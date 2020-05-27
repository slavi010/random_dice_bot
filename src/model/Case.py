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

    def is_mimic_dice(self, image):
        color = image[self.y + int(self.height*10/50)][self.x]
        # print('joker color : ' + str(color))
        return same_color_offset_rgb(color, (236, 192, 246), offset_rgb=(15, 15, 15))

    def get_dot_dice(self, image, is_multi_color: bool):
        #
        # *   * (0     1)
        # * * * (2  3  4)
        # *   * (5     6)
        #
        x_offset = int(self.width / 5)
        y_offset = int(self.height / 5)
        dots_color = [image[coord[1]][coord[0]] for coord in self.coord_all_dots()]

        if not is_multi_color:
            # 1* or 7*
            tmp_dots = dots_color.copy()
            tmp_dots.pop(3)
            if not is_dots_dice(tmp_dots):
                return 7 if self.is_star(image) else 1, dots_color[3]

            # 2*
            tmp_dots = dots_color.copy()
            tmp_dots.pop(1)
            tmp_dots.pop(5 - 1)
            if not is_dots_dice(tmp_dots):
                return 2, dots_color[1]

            # 3*
            tmp_dots = dots_color.copy()
            tmp_dots.pop(1)
            tmp_dots.pop(3 - 1)
            tmp_dots.pop(5 - 2)
            if not is_dots_dice(tmp_dots):
                return 3, dots_color[3]

            # 4*
            tmp_dots = dots_color.copy()
            tmp_dots.pop(0)
            tmp_dots.pop(1 - 1)
            tmp_dots.pop(5 - 2)
            tmp_dots.pop(6 - 3)
            if not is_dots_dice(tmp_dots):
                return 4, dots_color[1]

            # 5*
            tmp_dots = dots_color.copy()
            tmp_dots.pop(0)
            tmp_dots.pop(1 - 1)
            tmp_dots.pop(3 - 2)
            tmp_dots.pop(5 - 3)
            tmp_dots.pop(6 - 4)
            if not is_dots_dice(tmp_dots):
                return 5, dots_color[3]

            return 6, dots_color[1]
        else:
            # 1* or 7*
            tmp_dots = dots_color.copy()
            if not is_dots_same_color(tmp_dots):
                return 7 if self.is_star(image) else 1, None

            # 2*
            if not is_dots_same_color([dots_color[0], dots_color[1], dots_color[3]]):
                return 2, None

            # 3*
            if not is_dots_same_color([dots_color[0], dots_color[1]]):
                return 3, None

            # 4*
            if not is_dots_same_color([dots_color[1], dots_color[2], dots_color[3]]):
                return 4, None

            # 5*
            if not is_dots_same_color([dots_color[1], dots_color[2]]):
                return 5, None

            # TODO : 7

            return 6, None

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

    def is_star(self, image):
        x_offset = int(self.width / 6.8)
        y_offset = int(self.height / 6.8)
        image = image[self.y-y_offset:self.y+y_offset, self.x-x_offset:self.x+x_offset]
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        edges = cv2.Canny(gray, 100, 100*3)

        # on prend les contours
        ret, thresh = cv2.threshold(edges.copy(),
                                    0,
                                    255,
                                    cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        div_max_size = 0.23
        div_min_size = 0.2
        for contour in contours:
            # print(np.sqrt(cv2.contourArea(contour))/cv2.arcLength(contour, True))
            area = cv2.contourArea(contour)
            if div_max_size > np.sqrt(area)/cv2.arcLength(contour, True) > div_min_size and \
                    area > x_offset*y_offset*4/2:
                cv2.imshow("cv2", image)
                cv2.waitKey(1)
                return True

        return False

    def __str__(self):
        return '({0} {1}) {2}'.format(self.x, self.y, self.dice)


def is_dots_dice(dots_color):
    for dot_idx in range(len(dots_color)):
        for name, member in DiceColorEnum.__members__.items():
            for color in member.value[1]:
                if same_color(dots_color[dot_idx], color):
                    return True

    return False

def is_dots_same_color(dots_color):
    for dot_idx in range(len(dots_color)):
        if not (dots_color[dot_idx][0] > 250 and dots_color[dot_idx][1] > 250 and dots_color[dot_idx][2] > 250):
            # pas blanc
            for j in range(dot_idx+1, len(dots_color)):
                if same_color(dots_color[dot_idx], dots_color[j]):
                    return True

    return False