import random
from time import sleep

import cv2 as cv2
import numpy as np

from src.model.Case import Case
from src.controller.MouseEvent import get_next_click_mouse

from PIL import Image, ImageGrab

from ahk import AHK

from src.model.Dice import Dice
from src.model.DiceEnum import DiceColorEnum
from src.model.Utils import same_color, same_color_hsv


class Plateau:
    def __init__(self, ahk: AHK):
        self.ahk = ahk

        # get position premier dé en haut à gauche
        x_1, y_1, _, _ = get_next_click_mouse()

        sleep(0.5)
        # get position dernier dé en bas à droite
        x_2, y_2, _, _ = get_next_click_mouse()

        width_dice = int((x_2 - x_1) / 4)
        height_dice = int((y_2 - y_1) / 2)
        print('width_dice={0}, height_dice={1}'.format(width_dice, height_dice))

        self.cases = [[Case(j * width_dice + x_1, i * height_dice + y_1, width_dice, height_dice) for j in range(5)] for
                      i in range(3)]

        self.screen_size = (1920, 1080)

        self.btn_coord_add_dice = (x_1 + width_dice * 2, y_2 + int(height_dice * 2.6))
        self.btn_coord_buy_shop = []
        for i in range(5):
            self.btn_coord_buy_shop.append(
                (x_1 - int(width_dice * 4 / 5) + i * int(width_dice * 1.43), y_2 + int(height_dice * 4.3)))

    def scan(self):
        """Met à jours les dés présents"""
        image = grab_image(box=(0, 0, self.screen_size[0], self.screen_size[1]))

        range_color = 15

        compteur = 0
        for case_row in self.cases:
            for case in case_row:
                compteur += 1
                # print(str(compteur) + " " + str(case.get_average_color(image)))

                avg_color = case.get_average_color(image)
                case.dice = None

                # assigne un dé à la case si les couleurs correspondes
                if not same_color(avg_color, (219, 219, 219), offset=1) and \
                        not same_color(avg_color, (110, 0, 63), offset=1):  # couleur du plateau de base ?
                    nb_dot, color_dot = case.get_dot_dice(image)
                    print(str(nb_dot) + " " + str(color_dot))
                    for name, member in DiceColorEnum.__members__.items():
                        for color in member.value:
                            if same_color(color, color_dot):
                                case.dice = Dice(member, nb_dot)

                print(case.__str__())
        print("#######################")
        self.show(image)

    def get_nb_cases_vide(self):
        cases_vides = 0
        for case_row in self.cases:
            for case in case_row:
                if case.dice is None:
                    cases_vides += 1
        return cases_vides

    def add_dice(self):
        self.ahk.click(x=self.btn_coord_add_dice[0], y=self.btn_coord_add_dice[1], blocking=False)

    def buy_shop(self, dice: int):
        if dice <= 0 or dice > 5:
            raise Exception("dice position need to be in range of 1 to 5")
        self.ahk.click(x=self.btn_coord_buy_shop[dice - 1][0], y=self.btn_coord_buy_shop[dice - 1][1], blocking=False)

    def do_fusion(self, from_case: Case, to_case: Case):
        self.ahk.mouse_move(x=from_case.x, y=from_case.y)
        self.ahk.mouse_drag(x=to_case.x, y=to_case.y)

        # on reposition la sourie en IDLE
        self.ahk.mouse_move(x=self.cases[0][0].x - self.cases[0][0].width,
                            y=self.cases[0][0].y - self.cases[0][0].height)

    def get_possible_fusion(self):
        fusions = []

        for y1 in range(3):
            for x1 in range(5):
                if self.cases[y1][x1].dice is not None:
                    for y2 in range(3):
                        for x2 in range(5):

                            if self.cases[y2][x2].dice is not None and \
                                    self.cases[y1][x1].dice.dot == self.cases[y2][x2].dice.dot and \
                                    self.cases[y1][x1].dice.type_dice == self.cases[y2][x2].dice.type_dice and \
                                    (self.cases[y1][x1].x != self.cases[y2][x2].x or
                                     self.cases[y1][x1].y != self.cases[y2][x2].y):
                                fusions.append((self.cases[y1][x1], self.cases[y2][x2]))
        return fusions

    def show(self, image_raw):
        # on redimensionne l'image
        first_case = self.cases[0][0]
        last_case = self.cases[2][4]
        box = (first_case.x - first_case.width,
               first_case.y - first_case.height,
               last_case.x + last_case.width,
               last_case.y + last_case.height)
        # print('box ' + str(box))
        img = image_raw.copy()[box[1]:box[3], box[0]:box[2]]

        for case_row in self.cases:
            for case in case_row:
                box_case_coord = case.get_box_coord()
                cv2.rectangle(img,
                              (box_case_coord[0] - box[0], box_case_coord[1] - box[1]),
                              (box_case_coord[2] - box[0], box_case_coord[3] - box[1]),
                              color=(0, 0, 255))
                dots_case_coord = case.coord_all_dots()
                for dot in dots_case_coord:
                    img[dot[1] - box[1]][dot[0] - box[0]] = [0, 0, 255]

        cv2.imshow("show", img)


def pil_to_cv2(image_pil):
    return cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)


def grab_image(box=(0, 0, 1920, 1080)):
    width = box[2] - box[0]
    height = box[3] - box[1]
    return pil_to_cv2(ImageGrab.grab(bbox=box))
