#################################################################################
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR    #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,      #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE   #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER        #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, #
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE #
# SOFTWARE.                                                                     #
#################################################################################
#
# Contributors :
# Copyright (c) 2020 slavi010 pro@slavi.dev
#


import random
from operator import itemgetter
from time import sleep

import cv2 as cv2
import numpy as np

from src.controller import MouseEvent
from src.model.Case import Case

from PIL import Image, ImageGrab

from ahk import AHK

from src.model.Dice import Dice
from src.model.DiceEnum import DiceColorEnum, DiceEnum
from src.model.Merge import Merge
from src.model.Utils import same_color, same_color_hsv


class Plateau:
    def __init__(self, ahk: AHK):
        self.ahk = ahk

        # get position premier dé en haut à gauche et dernier dé en bas à droite
        x_1, y_1, x_2, y_2 = MouseEvent.grab_points_dice()

        width_dice = (x_2 - x_1) / 4
        height_dice = (y_2 - y_1) / 2
        print('width_dice={0}, height_dice={1}'.format(width_dice, height_dice))

        self.cases = [[Case(int(j * width_dice + x_1), int(i * height_dice + y_1), int(width_dice), int(height_dice)) for j in range(5)] for
                      i in range(3)]

        self.screen_size = (1920, 1080)

        # btn = (x, y)
        self.btn_coord_add_dice = (x_1 + int(width_dice * 2.05), y_2 + int(height_dice * 2.6))
        self.btn_coord_buy_shop = []
        for i in range(5):
            self.btn_coord_buy_shop.append(
                (x_1 - int(width_dice * 4 / 5) + i * int(width_dice * 1.43), y_2 + int(height_dice * 4.3)))
        self.btn_coord_coop_mode = (x_2 + int(width_dice/5), y_2 + int(height_dice * 2))
        self.btn_coord_coop_mode_pub = (x_2 + int(width_dice), y_2 + int(height_dice * 2))
        self.btn_coord_coop_mode_quick_match = (x_2, y_2 - int(height_dice))

        # check fin de manche
        self.coord_end = (x_1 + int(width_dice*8/5), y_1 - int(height_dice))

    def scan_many_time(self, nb_scan, time_between_two_scan_ms=10):
        occurence_dice = [[] for i in range(15)] # [[(dice, occurence)]]
        for i in range(nb_scan):
            sleep(time_between_two_scan_ms/1000)
            self.scan()
            # on ajoute pour chaque case
            for case_y in range(3):
                for case_x in range(5):
                    # si le dé n'est pas null
                    if self.cases[case_y][case_x].dice is not None:
                        # on cherche si le dé est déjà présent
                        flag_dice_deja_present = False
                        for dice_and_occurence in occurence_dice[case_y*5 + case_x]:
                            if dice_and_occurence[0] == self.cases[case_y][case_x].dice:
                                dice_and_occurence[1] += 1
                                flag_dice_deja_present = True
                        # l'occurence n'est pas encore présente alors on la crée
                        if not flag_dice_deja_present:
                            occurence_dice[case_y*5 + case_x].append([self.cases[case_y][case_x].dice, 1])

        # on fait la "moyenne"
        for case_idx in range(15):
            # on trie avec les dés qui ont un occurance la plus forte en premier
            occurence_dice[case_idx].sort(key=itemgetter(1), reverse=True)
            # il y a moins de 33% d'un même dé alors None
            if len(occurence_dice[case_idx]) == 0 or occurence_dice[case_idx][0][1] < nb_scan/3:
                self.cases[int(case_idx/5)][case_idx%5].dice = None
            else:
                self.cases[int(case_idx/5)][case_idx%5].dice = occurence_dice[case_idx][0][0]

        image = grab_image(box=(0, 0, self.screen_size[0], self.screen_size[1]))
        self.show(image)

    def scan(self):
        """Met à jour les dés présents"""
        image = grab_image(box=(0, 0, self.screen_size[0], self.screen_size[1]))

        range_color = 15

        # compteur = 0
        for case_row in self.cases:
            for case in case_row:
                # compteur += 1
                # print(str(compteur) + " " + str(case.get_average_color(image)))

                avg_color = case.get_average_color(image)
                case.dice = None

                # assigne un dé à la case si les couleurs correspondes
                if not same_color(avg_color, (220, 220, 220), offset=3):  # couleur du plateau de base

                    if case.is_joker_dice(image):
                        nb_dot, color_dot = case.get_dot_dice(image, True)
                        # print(str(nb_dot) + " " + str(color_dot))
                        case.dice = Dice(DiceColorEnum.JOKER, nb_dot)
                    elif case.is_mimic_dice(image):
                        nb_dot, color_dot = case.get_dot_dice(image, True)
                        # print(str(nb_dot) + " " + str(color_dot))
                        case.dice = Dice(DiceColorEnum.MIMIC, nb_dot)
                    else:
                        nb_dot, color_dot = case.get_dot_dice(image, False)
                        # print(str(nb_dot) + " " + str(color_dot))
                        for name, member in DiceColorEnum.__members__.items():
                            for color in member.value[1]:
                                if same_color(color, color_dot):
                                    case.dice = Dice(member, nb_dot)

                # print(case.__str__())

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

    def do_merge(self, merge: Merge):
        self.ahk.mouse_move(x=merge.from_case.x, y=merge.from_case.y, speed=3)
        sleep(0.1)
        self.ahk.mouse_drag(x=merge.to_case.x, y=merge.to_case.y)

        # on reposition la sourie en IDLE
        self.ahk.mouse_move(x=self.cases[0][0].x - self.cases[0][0].width,
                            y=self.cases[0][0].y - self.cases[0][0].height,
                            speed=3)
        sleep(0.1)

    def get_possible_merge(self, shuffle=True):
        merges = []
        cases = np.reshape(self.cases.copy(), 15)

        for idx_1 in range(15):
            if cases[idx_1].dice is not None:
                for idx_2 in range(15):
                    if cases[idx_2].dice is not None and \
                            cases[idx_1] == cases[idx_2].dice.dot and \
                            (cases[idx_1].dice.type_equal(cases[idx_2].dice) or
                             cases[idx_1] == [DiceColorEnum.JOKER, DiceColorEnum.MIMIC] or
                             cases[idx_2] == DiceColorEnum.MIMIC) and \
                            (not cases[idx_1] == cases[idx_2]):
                        merges.append(Merge(cases[idx_1], cases[idx_2]))
        if shuffle:
            random.shuffle(merges)
        return merges

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
        cv2.waitKey(1)

    def is_dice_ready_to_merge(self, merges, dice: DiceColorEnum):
        for merge in merges:
            if merge.from_case == dice and \
                    merge.to_case == dice:
                self.do_merge(merge)
                merges.remove(merge)

                # on supprime la fusion inverse
                for m in merges:
                    if merge.from_case == m.to_case and \
                            merge.to_case == m.from_case:
                        merges.remove(m)
                        break

    def is_coop_ready(self, image):
        return same_color(image[self.btn_coord_coop_mode[1]][self.btn_coord_coop_mode[0]],
                          (255, 213, 165), offset=2)

    def start_pub(self):
        self.ahk.click(x=self.btn_coord_coop_mode_pub[0], y=self.btn_coord_coop_mode_pub[1], blocking=False)

    def start_coop(self):
        self.ahk.click(x=self.btn_coord_coop_mode[0], y=self.btn_coord_coop_mode[1], blocking=False)
        sleep(1)
        self.ahk.click(x=self.btn_coord_coop_mode_quick_match[0], y=self.btn_coord_coop_mode_quick_match[1], blocking=False)

    def is_end(self, image):
        return same_color(image[self.coord_end[1]][self.coord_end[0]],
                          (239, 173, 51), offset=30) or \
               not same_color(image[self.btn_coord_add_dice[1]][self.btn_coord_add_dice[0]],
                          (250, 250, 250), offset=6)


def pil_to_cv2(image_pil):
    return cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)


def grab_image(box=(0, 0, 1920, 1080)):
    width = box[2] - box[0]
    height = box[3] - box[1]
    return pil_to_cv2(ImageGrab.grab(bbox=box))
