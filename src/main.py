import random
from time import sleep

import cv2
from pynput.mouse import Listener

from src.model.Plateau import Plateau

from ahk import AHK

if __name__ == '__main__':
    ahk = AHK()
    plateau = Plateau(ahk)
    sleep(1)
    plateau.scan()

    # k = cv2.waitKey(0)

    while True:
        plateau.scan()
        print('case vide = {}'.format(plateau.get_nb_cases_vide()))
        while plateau.get_nb_cases_vide() > random.randint(0, 1):
            sleep(0.1 + random.random()*0.5)
            plateau.scan()
            plateau.add_dice()
            cv2.waitKey(1)
        sleep(0.1 + random.random()*0.5)

        fusions = plateau.get_possible_fusion()
        while random.random() < 0.5:
            if len(fusions) > 0:
                lower_fusion = fusions[0]
                for fusion in fusions:
                    if fusion[0].dice.dot < lower_fusion[0].dice.dot:
                        lower_fusion = fusion
                plateau.do_fusion(lower_fusion[0], lower_fusion[1])
                fusions.remove(lower_fusion)
                cv2.waitKey(1)


    # for i in range(1, 6):
    #     plateau.buy_shop(i)
    #     sleep(1)

