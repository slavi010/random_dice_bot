import random
from time import sleep

import cv2
from pynput.mouse import Listener

from src.model.DiceEnum import DiceColorEnum
from src.model.FeaturePlateau import FeaturePlateau
from src.model.Plateau import Plateau

from ahk import AHK

if __name__ == '__main__':
    ahk = AHK()
    plateau = Plateau(ahk)
    feature = FeaturePlateau(plateau) \
        .add_auto_fill_board() \
        .add_fusion_sacrifice_during_auto_fill_board() \
        .add_buy_shop_during_auto_fill_board() \
        .add_sleep_random() \
        .add_auto_merge() \
        .add_fusion_joker_to_other_dice_during_auto_merge(dice=DiceColorEnum.SACRIFICIAL) \
        .add_merge_random_lower_during_auto_merge(dices=[DiceColorEnum.SACRIFICIAL,
                                                         DiceColorEnum.IRON,
                                                         DiceColorEnum.ICE,
                                                         DiceColorEnum.LOCK])
    plateau.feature = feature

    sleep(1)
    plateau.scan()

    # k = cv2.waitKey(0)

    while True:
        print('case vide = {}'.format(plateau.get_nb_cases_vide()))
        plateau.scan()

        plateau.feature.start_features()
        sleep(1)
