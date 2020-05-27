import random
from time import sleep

import numpy as np

from src.model.DiceEnum import DiceColorEnum
from src.model.Plateau import Plateau


class FeaturePlateau:
    def __init__(self, plateau: Plateau):
        self.plateau = plateau

        self.features = []
        self.sub_features = []

    def start_features(self):
        for feature in self.features:
            feature()
        return self

    # 0
    def add_fusion_sacrifice(self):
        self.features.append(lambda: self.plateau.is_sacrifice_ready_to_merge(self.plateau.get_possible_fusion()))
        return self

    # 1
    def add_buy_shop(self, proba_buy_shop: float, idx_dices=None):
        self.features.append(lambda: self.callback_buy_shop(proba_buy_shop, idx_dices))
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
    def add_fusion_joker_to_other_dice(self, dice=None):
        self.features.append(lambda: self.callback_fusion_joker_to_other_dice(dice))
        return self

    # 4
    def add_add_dice(self):
        self.features.append(lambda: self.callback_add_dice())
        return self

    def add_fusion_combo(self):
        self.features.append(lambda: self.callback_fusion_combo())
        return self

    def callback_add_dice(self):
        self.plateau.scan()
        self.plateau.add_dice()

    def callback_buy_shop(self, proba_buy_shop: float, idx_dices=None):
        idx_dice_to_buy = random.randint(1, 5)
        while idx_dice_to_buy not in idx_dices and idx_dices is not None:
            idx_dice_to_buy = random.randint(1, 5)

        while random.random() < proba_buy_shop:
            sleep(1)
            self.plateau.buy_shop(idx_dice_to_buy)

    def callback_merge_random_lower(self, dices=None, min_dice_present=15):
        if 15 - self.plateau.get_nb_cases_vide() >= min_dice_present:
            fusions = self.plateau.get_possible_fusion()
            fusions = random.shuffle(fusions)
            if fusions is not None and len(fusions) > 0:
                lower_fusion = fusions[0]
                for fusion in fusions:
                    # si bon dice à merge
                    if dices[1] is None or fusion[0].dice.type_dice in dices:
                        if fusion[0].dice.dot < lower_fusion[0].dice.dot:
                            lower_fusion = fusion
                self.plateau.do_fusion(lower_fusion[0], lower_fusion[1])
                fusions.remove(lower_fusion)

    def callback_fusion_joker_to_other_dice(self, dice):
        fusions = self.plateau.get_possible_fusion()
        for fusion in fusions:
            if fusion[0].dice.type_dice == DiceColorEnum.JOKER and \
                    fusion[1].dice.type_dice == dice:
                self.plateau.do_fusion(fusion[0], fusion[1])
                fusions.remove(fusion)

    def callback_fusion_combo(self):
        fusions = self.plateau.get_possible_fusion()

        # # on supprime les fusions doublons
        # for fusion_1 in fusions:
        #     for fusion_2 in fusions:
        #         if fusion_1[0] == fusion_2[1] and \
        #                 fusion_1[1] == fusion_2[0]:
        #             fusions.remove(fusion_2)

        # on calcul le nombre de combo et de mimic pour chaque *
        nb_combos = [0 for i in range(7)]
        nb_mimic = [0 for i in range(7)]

        for case_row in self.plateau.cases:
            for case in case_row:
                if case.dice is not None:
                    if case.dice.type_dice == DiceColorEnum.COMBO:
                        nb_combos[case.dice.dot] += 1
                    elif case.dice.type_dice == DiceColorEnum.MIMIC:
                        nb_mimic[case.dice.dot] += 1

        # on fusion si min (2 combo + 1 mimic) ou (3 combo)
        for etoile in range(6):
            if nb_combos[etoile] >= 2 and nb_mimic[etoile] >= 1:
                for fusion in fusions:
                    if fusion[0].dice.type_dice == DiceColorEnum.COMBO and \
                            fusion[1].dice.type_dice == DiceColorEnum.MIMIC:
                        self.plateau.do_fusion(fusion[0], fusion[1])
                        break
                break
            elif nb_combos[etoile] >= 3:
                for fusion in fusions:
                    if fusion[0].dice.type_dice == DiceColorEnum.COMBO and \
                            fusion[1].dice.type_dice == DiceColorEnum.COMBO:
                        self.plateau.do_fusion(fusion[0], fusion[1])
                        break
                break
