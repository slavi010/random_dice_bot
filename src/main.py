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

import cv2
from pynput.mouse import Listener

from src.model.DiceEnum import DiceColorEnum
from src.model.FeaturePlateau import FeaturePlateau
from src.model.Plateau import Plateau, grab_image

from ahk import AHK

if __name__ == '__main__':
    # ahk is use for do click, mouse drag and auto ad
    ahk = AHK()

    # the board / the bot
    plateau = Plateau(ahk)

    # The bot actions
    feature = FeaturePlateau(plateau) \
        .add_add_dice() \
        .add_sleep_random(callback_random_float=lambda: sleep(0.1 + random.random() * 0.5)) \
        .add_merge_joker_to_other_dice(dice=DiceColorEnum.COMBO) \
        .add_merge_joker_to_other_dice(dice=DiceColorEnum.SACRIFICIAL, min_joker=2, merge_all=False) \
        .add_merge_dice(dice=DiceColorEnum.SACRIFICIAL) \
        .add_merge_dice(dice=DiceColorEnum.METASTASIS) \
        .add_buy_shop(proba_buy_shop=0.05, idx_dices=[5], min_dice_board=8) \
        .add_merge_combo(max_dot_merge=4) \
        .add_merge_random_lower(dices=[DiceColorEnum.SACRIFICIAL,
                                       DiceColorEnum.MIMIC],
                                min_dice_present=15) \
        .add_auto_pub_and_start(ahk)

    # we add feature of the bot to the board
    plateau.feature = feature

    # for debug if you want to make a break
    # and see the position of the red grid
    # plateau.scan()
    # k = cv2.waitKey(0)

    # the bot spawn his first dices
    for i in range(10):
        plateau.add_dice()
        sleep(0.1)

    # loop infinite
    while True:
        # we scan the board to detect all dice
        # more the nb_scan is high, more this take time (and CPU)
        plateau.scan_many_time(nb_scan=10)

        # we iterate one time all features
        plateau.feature.start_features()

        # stop the bot with the Escape key
        if ahk.key_state('Escape'):
            break

print("BOT IS OFF")
