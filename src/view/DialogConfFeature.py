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
import tkinter as tk
from typing import Dict, Union

from src.model.DiceEnum import DiceColorEnum
from src.model.FeaturePlateau import merge_dice_feature, buy_upgrade_feature
from src.view.Deck import Deck
from src.view.DialogWidget import FieldInt, ListDice, FieldRadioBinary


class DiceMergeFeatureConfDialog:
    """
    The config dialog for the dice_merge feature.
    """
    def __init__(self, deck: Deck, frame: bool, returning: Union[Dict, None]):
        # https://stackoverflow.com/questions/10057672/correct-way-to-implement-a-custom-popup-tkinter-dialog-box
        self.root = tk.Tk()
        self.deck = deck
        self.root.title('Merge dice feature')
        # remove the outer frame if frame=False
        if not frame: self.root.overrideredirect(True)

        # call self.close_mod when the close button is pressed
        self.root.protocol("WM_DELETE_WINDOW", self.close_mod)

        # The returning value
        if returning is not None:
            self.returning = returning
        else:
            self.returning = {
                "lst_from": [],
                "lst_to": [],
                "min_dices_board": 2,
                "max_dices_board": 15,
                "min_dots": 1,
                "max_dots": 7,
                "min_dices_from": 1,
                "min_dices_to": 15,
                "merge_priority": 1,
            }

        # Frame
        self.frm_lst = tk.Frame(self.root)
        self.frm_min_max = tk.Frame(self.root)
        self.frm_rad = tk.Frame(self.root)
        # save
        self.btn_save = tk.Button(self.root, width=8, text="Save")
        self.btn_save['command'] = self.btn_save_action

        # Frame layout
        self.frm_lst.grid(row=0, column=0)
        self.frm_min_max.grid(row=1, column=0)
        self.frm_rad.grid(row=2, column=0)
        self.btn_save.grid(row=3, column=0)

        # dice chose
        self.lst_from = ListDice(self.frm_lst, deck, "from",
                                 self.deck.get_index_dices(self.returning.get("lst_from")))
        self.lst_to = ListDice(self.frm_lst, deck, "to",
                               self.deck.get_index_dices(self.returning.get("lst_to")))
        self.deck.attach(self.lst_from)
        self.deck.attach(self.lst_to)
        # min max
        self.fld_min_dices_board = FieldInt(self.frm_min_max, "min dice board: ", 2, self.returning.get('min_dices_board'), 15)
        self.fld_max_dices_board = FieldInt(self.frm_min_max, "max dice board: ", 2, self.returning.get('max_dices_board'), 15)
        self.fld_min_dots = FieldInt(self.frm_min_max, "min dots dice: ", 1, self.returning.get('min_dots'), 7)
        self.fld_max_dots = FieldInt(self.frm_min_max, "max dots dice: ", 1, self.returning.get('max_dots'), 7)
        self.fld_min_dices_from = FieldInt(self.frm_min_max, "min dices from: ", 1, self.returning.get('min_dices_from'), 15)
        self.fld_min_dices_to = FieldInt(self.frm_min_max, "max dices to: ", 1, self.returning.get('min_dices_to'), 15)
        # radio
        self.rad_merge_priority = FieldRadioBinary(self.frm_rad, "merge priority: ", "lower", "random", self.returning.get('merge_priority'))

        # layouts
        self.lst_from.frm.grid(row=0, column=0)
        self.lst_to.frm.grid(row=0, column=1)
        self.fld_min_dices_board.frm.grid(row=0, column=0)
        self.fld_max_dices_board.frm.grid(row=0, column=1)
        self.fld_min_dots.frm.grid(row=1, column=0)
        self.fld_max_dots.frm.grid(row=1, column=1)
        self.fld_min_dices_from.frm.grid(row=2, column=0)
        self.fld_min_dices_to.frm.grid(row=2, column=1)
        self.rad_merge_priority.frm.grid(row=0, column=0)

        # a trick to activate the window (on windows 7)
        # self.root.deiconify()
        self.root.mainloop()

    # remove this function and the call to protocol
    # then the close button will act normally
    def close_mod(self):
        self.root.quit()
        self.root.destroy()

    def btn_save_action(self, event=None):
        self.returning = {
            "lst_from": self.lst_from.get_selected_dices(),
            "lst_to": self.lst_to.get_selected_dices(),
            "min_dices_board": self.fld_min_dices_board.get_value(),
            "max_dices_board": self.fld_max_dices_board.get_value(),
            "min_dots": self.fld_min_dots.get_value(),
            "max_dots": self.fld_max_dots.get_value(),
            "min_dices_from": self.fld_min_dices_from.get_value(),
            "min_dices_to": self.fld_min_dices_to.get_value(),
            "merge_priority": self.rad_merge_priority.get_value(),
        }
        self.root.quit()
        self.root.destroy()


class BuyUpgradeFeatureConfDialog:
    """
    The config dialog for the buy_upgrade feature.
    """
    def __init__(self, deck: Deck, frame: bool, returning: Union[Dict, None]):
        # https://stackoverflow.com/questions/10057672/correct-way-to-implement-a-custom-popup-tkinter-dialog-box
        self.root = tk.Tk()
        self.deck = deck
        self.root.title('Buy upgrade feature')
        # remove the outer frame if frame=False
        if not frame: self.root.overrideredirect(True)

        # call self.close_mod when the close button is pressed
        self.root.protocol("WM_DELETE_WINDOW", self.close_mod)

        # The returning value
        if returning is not None:
            self.returning = returning
        else:
            self.returning = {
                "lst_index_dice": [],
                "proba_buy_upgrade": 0.05,
                "min_dices_board": 8,
            }

        # Frame
        self.frm_lst = tk.Frame(self.root)
        self.frm_field = tk.Frame(self.root)
        # save
        self.btn_save = tk.Button(self.root, width=8, text="Save")
        self.btn_save['command'] = self.btn_save_action

        # Frame layout
        self.frm_lst.grid(row=0, column=0)
        self.frm_field.grid(row=1, column=0)
        self.btn_save.grid(row=2, column=0)

        # dice chose
        self.lst = ListDice(self.frm_lst, deck, "from", self.returning.get("lst_index_dice"))
        self.deck.attach(self.lst)

        # Field
        self.fld_proba_buy_upgrade = FieldInt(
            self.frm_field, "Proba buy upgrade (%): ", 0, int(self.returning.get("proba_buy_upgrade")*100), 100
        )
        self.fld_min_dice_board = FieldInt(
            self.frm_field, "Min dice board: ", 0, self.returning.get("min_dices_board"), 15
        )

        # layouts
        self.lst.frm.grid(row=0, column=0)
        self.fld_proba_buy_upgrade.frm.grid(row=0, column=0)
        self.fld_min_dice_board.frm.grid(row=1, column=0)

        # a trick to activate the window (on windows 7)
        # self.root.deiconify()
        self.root.mainloop()

    # remove this function and the call to protocol
    # then the close button will act normally
    def close_mod(self):
        self.root.quit()
        self.root.destroy()

    def btn_save_action(self, event=None):
        self.returning = {
            "lst_index_dice": self.deck.get_index_dices(self.lst.get_selected_dices()),
            "proba_buy_upgrade": self.fld_proba_buy_upgrade.get_value() / 100.0,
            "min_dices_board": self.fld_min_dice_board.get_value(),
        }
        self.root.quit()
        self.root.destroy()
class BuyUpgradeFeatureConfDialog:
    """
    The config dialog for the buy_upgrade feature.
    """
    def __init__(self, deck: Deck, frame: bool, returning: Union[Dict, None]):
        # https://stackoverflow.com/questions/10057672/correct-way-to-implement-a-custom-popup-tkinter-dialog-box
        self.root = tk.Tk()
        self.deck = deck
        self.root.title('Buy upgrade feature')
        # remove the outer frame if frame=False
        if not frame: self.root.overrideredirect(True)

        # call self.close_mod when the close button is pressed
        self.root.protocol("WM_DELETE_WINDOW", self.close_mod)

        # The returning value
        if returning is not None:
            self.returning = returning
        else:
            self.returning = {
                "lst_index_dice": [],
                "proba_buy_upgrade": 0.05,
                "min_dices_board": 8,
            }

        # Frame
        self.frm_lst = tk.Frame(self.root)
        self.frm_field = tk.Frame(self.root)
        # save
        self.btn_save = tk.Button(self.root, width=8, text="Save")
        self.btn_save['command'] = self.btn_save_action

        # Frame layout
        self.frm_lst.grid(row=0, column=0)
        self.frm_field.grid(row=1, column=0)
        self.btn_save.grid(row=2, column=0)

        # dice chose
        self.lst = ListDice(self.frm_lst, deck, "from", self.returning.get("lst_index_dice"))
        self.deck.attach(self.lst)

        # Field
        self.fld_proba_buy_upgrade = FieldInt(
            self.frm_field, "Proba buy upgrade (%): ", 0, int(self.returning.get("proba_buy_upgrade")*100), 100
        )
        self.fld_min_dice_board = FieldInt(
            self.frm_field, "Min dice board: ", 0, self.returning.get("min_dices_board"), 15
        )

        # layouts
        self.lst.frm.grid(row=0, column=0)
        self.fld_proba_buy_upgrade.frm.grid(row=0, column=0)
        self.fld_min_dice_board.frm.grid(row=1, column=0)

        # a trick to activate the window (on windows 7)
        # self.root.deiconify()
        self.root.mainloop()

    # remove this function and the call to protocol
    # then the close button will act normally
    def close_mod(self):
        self.root.quit()
        self.root.destroy()

    def btn_save_action(self, event=None):
        self.returning = {
            "lst_index_dice": self.deck.get_index_dices(self.lst.get_selected_dices()),
            "proba_buy_upgrade": self.fld_proba_buy_upgrade.get_value() / 100.0,
            "min_dices_board": self.fld_min_dice_board.get_value(),
        }
        self.root.quit()
        self.root.destroy()
