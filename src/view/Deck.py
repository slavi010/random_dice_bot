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
from typing import List, Union
import tkinter as tk

from src.model.DiceEnum import DiceColorEnum
from src.model.FeaturePlateau import merge_dice_feature
from src.view.Observer import Observable, Observer


class Deck(Observable):
    _observers: List[Observer] = []

    dices: List[DiceColorEnum] = []

    def __init__(self, dices_default):
        self.dices = dices_default

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self)

    def get_index_dice(self, type_dice: DiceColorEnum):
        """
        :param type_dice:
        :return: int between 0-4 or None if not found
        """
        for idx, dice in enumerate(self.dices):
            if dice == type_dice:
                return idx
        return None

    def get_index_dices(self, type_dices: Union[tuple, list]):
        return [self.get_index_dice(type_dice) for type_dice in type_dices]


# root = tk.Tk()
#
# deck = Deck.py([DiceColorEnum.JOKER,
#              DiceColorEnum.GROWTH,
#              DiceColorEnum.MIMIC,
#              DiceColorEnum.SACRIFICIAL,
#              DiceColorEnum.COMBO])
#
# print()
#
# root.mainloop()
