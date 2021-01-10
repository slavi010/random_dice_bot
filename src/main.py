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

import tkinter as tk

import cv2
from pynput.mouse import Listener

from src.model.DiceEnum import DiceColorEnum
from src.model.FeaturePlateau import FeaturePlateau
from src.model.Plateau import Plateau, grab_image

from ahk import AHK

from src.view.MainDialog import MainDialog, MergeDiceFeatureView, BuyDiceFeatureView, BuyUpgradeFeatureView, \
    AutoAdFeatureView

if __name__ == '__main__':
    # ahk is use for do click, mouse drag and auto ad
    ahk = AHK()

    main_dialog = MainDialog(tk.Tk(), ahk)

    # auto ad
    main_dialog.add_feature(AutoAdFeatureView(main_dialog.frm_feature, ahk))

    # buy dice
    main_dialog.add_feature(BuyDiceFeatureView(main_dialog.frm_feature))

    # buy
    main_dialog.add_feature(BuyUpgradeFeatureView(main_dialog.frm_feature,
                                                  main_dialog.deck,
                                                  {
                                                      "name": "Combo",
                                                      "lst_index_dice": [5],
                                                      "proba_buy_upgrade": 0.05,
                                                      "min_dices_board": 8,
                                                  }))

    # merge JOKER-COMBO
    main_dialog.add_feature(MergeDiceFeatureView(main_dialog.frm_feature,
                                                 main_dialog.deck,
                                                 {
                                                     "name": "JOKER-COMBO",
                                                     "lst_from": [DiceColorEnum.JOKER],
                                                     "lst_to": [DiceColorEnum.COMBO],
                                                     "min_dices_board": 2,
                                                     "max_dices_board": 15,
                                                     "min_dots": 1,
                                                     "max_dots": 7,
                                                     "min_dices_from": 1,
                                                     "min_dices_to": 1,
                                                     "merge_priority": 1,
                                                 }))

    # merge SACRIFICIAL-SACRIFICIAL
    main_dialog.add_feature(MergeDiceFeatureView(main_dialog.frm_feature,
                                                 main_dialog.deck,
                                                 {
                                                     "name": "METASTASIS-METASTASIS",
                                                     "lst_from": [DiceColorEnum.METASTASIS],
                                                     "lst_to": [DiceColorEnum.METASTASIS],
                                                     "min_dices_board": 2,
                                                     "max_dices_board": 15,
                                                     "min_dots": 1,
                                                     "max_dots": 5,
                                                     "min_dices_from": 1,
                                                     "min_dices_to": 1,
                                                     "merge_priority": 1,
                                                 }))

    # merge COMBO-MIMIC
    main_dialog.add_feature(MergeDiceFeatureView(main_dialog.frm_feature,
                                                 main_dialog.deck,
                                                 {
                                                     "name": "COMBO-MIMIC",
                                                     "lst_from": [DiceColorEnum.COMBO],
                                                     "lst_to": [DiceColorEnum.MIMIC],
                                                     "min_dices_board": 8,
                                                     "max_dices_board": 15,
                                                     "min_dots": 1,
                                                     "max_dots": 5,
                                                     "min_dices_from": 2,
                                                     "min_dices_to": 1,
                                                     "merge_priority": 1,
                                                 }))

    # merge COMBO-COMBO
    main_dialog.add_feature(MergeDiceFeatureView(main_dialog.frm_feature,
                                                 main_dialog.deck,
                                                 {
                                                     "name": "COMBO-COMBO",
                                                     "lst_from": [DiceColorEnum.COMBO],
                                                     "lst_to": [DiceColorEnum.COMBO],
                                                     "min_dices_board": 9,
                                                     "max_dices_board": 15,
                                                     "min_dots": 1,
                                                     "max_dots": 4,
                                                     "min_dices_from": 3,
                                                     "min_dices_to": 1,
                                                     "merge_priority": 1,
                                                 }))

    # merge OTHER when board full
    main_dialog.add_feature(MergeDiceFeatureView(main_dialog.frm_feature,
                                                 main_dialog.deck,
                                                 {
                                                     "name": "board full",
                                                     "lst_from": [DiceColorEnum.MIMIC, DiceColorEnum.SACRIFICIAL],
                                                     "lst_to": [DiceColorEnum.MIMIC, DiceColorEnum.SACRIFICIAL],
                                                     "min_dices_board": 15,
                                                     "max_dices_board": 15,
                                                     "min_dots": 1,
                                                     "max_dots": 5,
                                                     "min_dices_from": 1,
                                                     "min_dices_to": 1,
                                                     "merge_priority": 1,
                                                 }))
    # merge ALL OTHER when board full
    main_dialog.add_feature(MergeDiceFeatureView(main_dialog.frm_feature,
                                                 main_dialog.deck,
                                                 {
                                                     "name": "board full",
                                                     "lst_from": main_dialog.deck.dices,
                                                     "lst_to": main_dialog.deck.dices,
                                                     "min_dices_board": 15,
                                                     "max_dices_board": 15,
                                                     "min_dots": 1,
                                                     "max_dots": 5,
                                                     "min_dices_from": 1,
                                                     "min_dices_to": 1,
                                                     "merge_priority": 1,
                                                 }))

    features = FeaturePlateau()
    features.features = [sub_feature_frm.get_callback_feature()
                         for sub_feature_frm in main_dialog.show_dialog().sub_feature_frms]

    # the board / the bot
    plateau = Plateau(ahk)

    # the bot spawn his first dices
    for i in range(10):
        plateau.add_dice()
        sleep(0.1)

    # loop infinite
    while True:
        # we scan the board to detect all dice
        # more the nb_scan is high, more this take time (and CPU)
        plateau.scan_many_time(nb_scan=4)

        # we iterate one time all features
        features.start_features(plateau)

        # stop the bot with the Escape key
        if ahk.key_state('Escape'):
            break

print("BOT IS OFF")
