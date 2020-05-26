import random
from time import sleep

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

    # sub 0
    def add_fusion_sacrifice_during_auto_fill_board(self):
        self.sub_features.append([0])
        return self

    # 1
    def add_auto_fill_board(self):
        self.features.append(lambda: self.callback_autofill_board())
        return self

    # sub 1
    def add_buy_shop_during_auto_fill_board(self):
        self.sub_features.append([1])
        return self

    # 2
    def add_auto_merge(self):
        self.features.append(lambda: self.callback_auto_merge())
        return self

    # sub 2
    def add_merge_random_lower_during_auto_merge(self, dices=None):
        self.sub_features.append([2, dices])
        return self

    # sub 3
    def add_fusion_sacrifice_during_auto_merge(self):
        self.sub_features.append([3])
        return self

    # 3
    def add_sleep_random(self):
        self.features.append(lambda: sleep(0.1 + random.random()*0.5))
        return self

    # sub 4
    def add_fusion_joker_to_other_dice_during_auto_merge(self, dice=None):
        self.sub_features.append([4, dice])
        return self

    def callback_autofill_board(self):
        while self.plateau.get_nb_cases_vide() > random.randint(0, 1):
            sleep(0.1 + random.random()*0.5)
            self.plateau.scan()
            self.plateau.add_dice()

            # merge sacrifice
            if len([features_idx[0] == 0 for features_idx in self.sub_features]) > 0:
                self.plateau.is_sacrifice_ready_to_merge(self.plateau.get_possible_fusion())

            # achat shop
            if len([features_idx[0] == 1 for features_idx in self.sub_features]) > 0:
                while random.random() < 0.1:
                    self.plateau.buy_shop(random.randint(1, 5))
                    sleep(1)

    def callback_auto_merge(self):
        fusions = self.plateau.get_possible_fusion()
        while random.random() < 0.5:
            if len(fusions) > 0:

                for sub_feature in self.sub_features:
                    # merge_random_lower
                    if sub_feature[0] == 2:
                        lower_fusion = fusions[0]
                        for fusion in fusions:
                            # si bon dice à merge
                            if sub_feature[1] is None or fusion[0].dice.type_dice in sub_feature[1]:
                                if fusion[0].dice.dot < lower_fusion[0].dice.dot:
                                    lower_fusion = fusion
                        self.plateau.do_fusion(lower_fusion[0], lower_fusion[1])
                        fusions.remove(lower_fusion)

                    # merge sacrifice
                    if sub_feature[0] == 3:
                        self.plateau.is_sacrifice_ready_to_merge(self.plateau.get_possible_fusion())

                    # fusion_joker_to_other_dice
                    if sub_feature[0] == 4:
                        for fusion in fusions:
                            if fusion[0].dice.type_dice == DiceColorEnum.JOKER and \
                                    fusion[1].dice.type_dice == sub_feature[1]:
                                self.plateau.do_fusion(fusion[0], fusion[1])
                                fusions.remove(fusion)

