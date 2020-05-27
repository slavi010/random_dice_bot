import random
from time import sleep

import cv2 as cv2
import numpy as np

from src.model.Case import Case
from src.controller.MouseEvent import get_next_click_mouse

from PIL import Image, ImageGrab

from ahk import AHK

from src.model.Dice import Dice
from src.model.DiceEnum import DiceColorEnum, DiceEnum
from src.model.Utils import same_color, same_color_hsv


class Plateau:
    def __init__(self, ahk: AHK):
        self.ahk = ahk
        self.feature = None

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
                if not same_color(avg_color, (220, 220, 220), offset=3):  # couleur du plateau de base

                    if case.is_joker_dice(image):
                        nb_dot, color_dot = case.get_dot_dice(image, True)
                        print(str(nb_dot) + " " + str(color_dot))
                        case.dice = Dice(DiceColorEnum.JOKER, nb_dot)
                    elif case.is_mimic_dice(image):
                        nb_dot, color_dot = case.get_dot_dice(image, True)
                        print(str(nb_dot) + " " + str(color_dot))
                        case.dice = Dice(DiceColorEnum.MIMIC, nb_dot)
                    else:
                        nb_dot, color_dot = case.get_dot_dice(image, False)
                        print(str(nb_dot) + " " + str(color_dot))
                        for name, member in DiceColorEnum.__members__.items():
                            for color in member.value[1]:
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
        cases = np.reshape(self.cases.copy(), 15)

        for idx_1 in range(15):
            if cases[idx_1].dice is not None:
                for idx_2 in range(15):
                    if cases[idx_2].dice is not None and \
                            cases[idx_1].dice.dot == cases[idx_2].dice.dot and \
                            (cases[idx_1].dice.type_dice == cases[idx_2].dice.type_dice or
                             cases[idx_1].dice.type_dice in [DiceColorEnum.JOKER, DiceColorEnum.MIMIC] or
                             cases[idx_2].dice.type_dice == DiceColorEnum.MIMIC) and \
                            (cases[idx_1].x != cases[idx_2].x or
                             cases[idx_1].y != cases[idx_2].y):
                        fusions.append((cases[idx_1], cases[idx_2]))
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
        cv2.waitKey(1)

        for case_row in self.cases:
            for case in case_row:
                box_case_coord = case.get_box_coord()
                cv2.rectangle(img,
                              (box_case_coord[0] - box[0], box_case_coord[1] - box[1]),
                              (box_case_coord[2] - box[0], box_case_coord[3] - box[1]),
                              color=(0, 0, 255))

                if case.dice is not None:
                    # affiche le nom du dé
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    bottomLeftCornerOfText = (
                    case.x - box[0] - int(case.width * 2 / 5), case.y - box[1] + int(case.height * 2 / 5))
                    fontScale = 0.3
                    fontColor = (0, 0, 0)
                    lineType = 1
                    cv2.putText(img, case.dice.type_dice.name,
                                bottomLeftCornerOfText,
                                font,
                                fontScale,
                                fontColor,
                                lineType)

                    # affiche le nombre du dé
                    bottomLeftCornerOfText = (
                    case.x - box[0] - int(case.width * 2 / 5), case.y - box[1] - int(case.height * 3 / 10))
                    cv2.putText(img, 'dot={0}'.format(case.dice.dot),
                                bottomLeftCornerOfText,
                                font,
                                fontScale,
                                fontColor,
                                lineType)

                dots_case_coord = case.coord_all_dots()
                for dot in dots_case_coord:
                    img[dot[1] - box[1]][dot[0] - box[0]] = [0, 0, 255]
                img[case.y + int(case.height * 10 / 50) - box[1]][case.x - box[0]] = [0, 0, 0]

        cv2.imshow("show", img)

    def is_sacrifice_ready_to_merge(self, fusions):
        for fusion in fusions:
            if fusion[0].dice.type_dice == DiceColorEnum.SACRIFICIAL and \
                    fusion[1].dice.type_dice == DiceColorEnum.SACRIFICIAL:
                self.do_fusion(fusion[0], fusion[1])
                fusions.remove(fusion)


def pil_to_cv2(image_pil):
    return cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)


def grab_image(box=(0, 0, 1920, 1080)):
    width = box[2] - box[0]
    height = box[3] - box[1]
    return pil_to_cv2(ImageGrab.grab(bbox=box))
