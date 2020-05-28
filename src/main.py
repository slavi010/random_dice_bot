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
    ahk = AHK()
    plateau = Plateau(ahk)
    feature = FeaturePlateau(plateau) \
        .add_add_dice() \
        .add_sleep_random(callback_random_float=lambda: sleep(0.1 + random.random() * 0.5)) \
        .add_fusion_joker_to_other_dice(dice=DiceColorEnum.COMBO) \
        .add_fusion_dice(dice=DiceColorEnum.SACRIFICIAL) \
        .add_fusion_dice(dice=DiceColorEnum.METASTASIS) \
        .add_buy_shop(proba_buy_shop=0.05, idx_dices=[5], min_dice_board=8) \
        .add_fusion_combo(max_dot_fusion=4) \
        .add_merge_random_lower(dices=[DiceColorEnum.SACRIFICIAL,
                                       DiceColorEnum.MIMIC],
                                min_dice_present=15) \
        .add_auto_pub_and_start(ahk)
    plateau.feature = feature

    sleep(1)
    # plateau.scan()

    # k = cv2.waitKey(0)
    for i in range(10):
        plateau.add_dice()
        sleep(0.1)

    while True:
        print('case vide = {}'.format(plateau.get_nb_cases_vide()))
        plateau.scan_many_time(nb_scan=10, time_between_two_scan_ms=10)

        print(plateau.is_coop_ready(grab_image()))

        plateau.feature.start_features()
        # sleep(1)
