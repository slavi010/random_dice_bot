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
from time import sleep

import numpy as np
from ahk import AHK

from src.model.DiceEnum import DiceColorEnum
from src.model.Plateau import Plateau, grab_image


class FeaturePlateau:
    def __init__(self, plateau: Plateau):
        self.plateau = plateau

        self.features = []

    def start_features(self):
        for feature in self.features:
            feature()
        return self

    # 0
    def add_merge_dice(self, dice: DiceColorEnum):
        self.features.append(lambda: self.plateau.is_dice_ready_to_merge(self.plateau.get_possible_merge(), dice))
        return self

    # 1
    def add_buy_shop(self, proba_buy_shop: float, idx_dices=None, min_dice_board=6):
        self.features.append(lambda: self.callback_buy_shop(proba_buy_shop, idx_dices, min_dice_board))
        return self

    # 2
    def add_merge_random_lower(self, dices=None, min_dice_present=15):
        self.features.append(lambda: self.callback_merge_random_lower(dices, min_dice_present))
        return self

    # 3
    def add_sleep_random(self, callback_random_float):
        # sleep(0.1 + random.random()*0.5)
        self.features.append(lambda: callback_random_float())
        return self

    # 5
    def add_merge_joker_to_other_dice(self, dice=None, min_joker=1, merge_all=True):
        self.features.append(lambda: self.callback_merge_joker_to_other_dice(dice, min_joker, merge_all))
        return self

    # 4
    def add_add_dice(self):
        self.features.append(lambda: self.callback_add_dice())
        return self

    # 6
    def add_auto_pub_and_start(self, ahk:AHK):
        self.features.append(lambda: self.callback_auto_pub_and_start(ahk=ahk))
        return self

    def add_merge_combo(self, max_dot_merge=4, min_dice_present=8):
        self.features.append(lambda: self.callback_merge_combo(max_dot_merge=max_dot_merge, min_dice_present=min_dice_present))
        return self

    def callback_add_dice(self, check_is_end=True, wait_time_sec=1):
        # self.plateau.scan()
        # sleep(wait_time_sec)
        if not check_is_end or not self.plateau.is_end(image=grab_image(box=(0, 0, self.plateau.screen_size[0], self.plateau.screen_size[1]))):
            self.plateau.add_dice()

    def callback_buy_shop(self, proba_buy_shop: float, idx_dices=None, min_dice_board=6):
        idx_dice_to_buy = random.randint(1, 5)
        if 15 - self.plateau.get_nb_cases_vide() >= min_dice_board:
            while idx_dice_to_buy not in idx_dices and idx_dices is not None:
                idx_dice_to_buy = random.randint(1, 5)

            while random.random() < proba_buy_shop:
                sleep(1)
                self.plateau.buy_shop(idx_dice_to_buy)

    def callback_merge_random_lower(self, dices=None, min_dice_present=15):
        if 15 - self.plateau.get_nb_cases_vide() >= min_dice_present:
            merges = self.plateau.get_possible_merge()
            if merges is not None and len(merges) > 0:
                lower_merge = merges[0]
                for merge in merges:
                    # si bon dice à merge
                    if dices is None or merge.from_case.dice.type_dice in dices:
                        if merge.from_case.dice < lower_merge.from_case.dice.dot:
                            lower_merge = merge
                self.plateau.do_merge(lower_merge)
                merges.remove(lower_merge)

    def callback_merge_joker_to_other_dice(self, dice, min_joker=1, merge_all=True):
        merges = self.plateau.get_possible_merge()

        # get number sacrifice
        # on calcule le nombre de joker pour chaque *
        nb_joker = [0 for i in range(7)]

        for case_row in self.plateau.cases:
            for case in case_row:
                if case.dice is not None:
                    if case == DiceColorEnum.JOKER:
                        nb_joker[case.dice.dot-1] += 1

        for merge in merges:
            if merge.from_case == DiceColorEnum.JOKER and \
                    merge.to_case == dice and \
                    nb_joker[merge.from_case.dice.dot-1] >= min_joker:
                self.plateau.do_merge(merge)
                merges.remove(merge)
                if not merge_all:
                    return

    def callback_merge_combo(self, max_dot_merge=4, min_dice_present=10):
        merges = self.plateau.get_possible_merge()

        # on calcule le nombre de combo et de mimic pour chaque *
        nb_combos = [0 for i in range(7)]
        nb_mimic = [0 for i in range(7)]

        for case_row in self.plateau.cases:
            for case in case_row:
                if case.dice is not None:
                    if case == DiceColorEnum.COMBO:
                        nb_combos[case.dice.dot-1] += 1
                    elif case == DiceColorEnum.MIMIC:
                        nb_mimic[case.dice.dot-1] += 1

        # Total des points
        # total_dot = 0
        # for i in range(7):
        #     total_dot += nb_combos[i] * (i + 1)

        if 15 - self.plateau.get_nb_cases_vide() >= min_dice_present:
            # on fusionne si min (2 combo + 1 mimic) ou (3 combo)
            flag_merge_done = False
            for etoile in range(6):
                if not flag_merge_done:
                    if nb_combos[etoile] >= 2 and nb_mimic[etoile] >= 1:
                        for merge in merges:
                            if ((merge.from_case == DiceColorEnum.COMBO and
                                        merge.to_case == DiceColorEnum.MIMIC) or
                                    (merge.from_case == DiceColorEnum.MIMIC and
                                        merge.to_case == DiceColorEnum.COMBO)
                                    ) and \
                                    merge.from_case == etoile+1 and \
                                    merge.from_case <= max_dot_merge:
                                self.plateau.do_merge(merge)
                                break
                        flag_merge_done = True
                    elif nb_combos[etoile] >= 3 and nb_mimic[etoile]  == 0:
                        for merge in merges:
                            if merge.from_case == DiceColorEnum.COMBO and \
                                    merge.to_case == DiceColorEnum.COMBO and \
                                    merge.from_case == etoile+1 and \
                                    merge.from_case <= max_dot_merge:
                                self.plateau.do_merge(merge)
                                break
                        flag_merge_done = True

    def callback_auto_pub_and_start(self, ahk:AHK):
        if self.plateau.is_end(image=grab_image(box=(0, 0, self.plateau.screen_size[0], self.plateau.screen_size[1]))):
            print("auto_pub_and_start")
            sleep(1)
            self.callback_add_dice(check_is_end=False)
            # attend chargement
            print("attend chargement")
            sleep(10)
            if not self.plateau.is_coop_ready(grab_image(box=(0, 0, self.plateau.screen_size[0], self.plateau.screen_size[1]))):
                # on regarde la pub
                self.plateau.start_pub()
                print("start pub")
                sleep(2)
                win = ahk.active_window
                while not self.plateau.is_coop_ready(grab_image(box=(0, 0, self.plateau.screen_size[0], self.plateau.screen_size[1]))):
                    print("attente fin de pub")
                    sleep(2)
                    # win.send('Escape')
                    script = "Send, {Escape}\n" + \
                             "Send, {Ctrl down}\n" + \
                             "Send, {Backspace}\n" + \
                             "Send, {Ctrl up}"
                    ahk.run_script(script)
                    sleep(2)
                print("pub fini")
            sleep(3)
            print("start coop")
            self.plateau.start_coop()
            sleep(12)
            for i in range(10):
                self.plateau.add_dice()
                sleep(0.1)
