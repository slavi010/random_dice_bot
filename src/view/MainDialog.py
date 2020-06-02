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
from abc import abstractmethod, ABC
from typing import Optional, Dict

import cv2
import numpy as np
from PIL import ImageTk, Image
from ahk import AHK

from src.model.DiceEnum import DiceColorEnum
from src.model.FeaturePlateau import merge_dice_feature, buy_upgrade_feature, buy_dice_feature
from src.model.Plateau import Plateau
from src.view.Deck import Deck
from src.view.DialogConfFeature import DiceMergeFeatureConfDialog, BuyUpgradeFeatureConfDialog


class MainDialog:
    """The main Dialog, with this dialog, you can change the deck and the bot actions"""

    def __init__(self, root):
        self.root = root

        # show this dialog
        self.show = False

        self.root.deiconify()

        # Frame
        self.frm_deck = tk.Frame(self.root, width=300, height=60, pady=3)
        self.frm_feature = tk.Frame(self.root, width=300, height=60, pady=3)
        self.frm_action = tk.Frame(self.root, width=300, height=60, pady=3)

        # Frame grid
        self.frm_deck.grid(row=0, sticky="ew")
        self.frm_feature.grid(row=1, sticky="ew")
        self.frm_action.grid(row=2, sticky="ew")

        # frm_deck widgets
        self.deck = Deck([DiceColorEnum.JOKER,
                          DiceColorEnum.GROWTH,
                          DiceColorEnum.MIMIC,
                          DiceColorEnum.SACRIFICIAL,
                          DiceColorEnum.COMBO])
        self.dices_canvas = []
        for i in range(5):
            canvas = tk.Canvas(self.frm_deck, width=50, height=50)
            self.dices_canvas.append(canvas)
        self.dices_canvas[0].bind("<Button-1>", lambda: self.change_dice_dialog(0))
        self.dices_canvas[1].bind("<Button-1>", lambda: self.change_dice_dialog(1))
        self.dices_canvas[2].bind("<Button-1>", lambda: self.change_dice_dialog(2))
        self.dices_canvas[3].bind("<Button-1>", lambda: self.change_dice_dialog(3))
        self.dices_canvas[4].bind("<Button-1>", lambda: self.change_dice_dialog(4))

        # frm_deck layout widgets
        for idx, dice_canvas in enumerate(self.dices_canvas):
            dice_canvas.grid(row=0, column=idx)

        # frm_feature widgets
        self.sub_feature_frms = []

        # frm_feature widgets layouts
        # self.update_frm_feature()

        # frm_action widgets
        self.btn_add_merge_dice_feature = tk.Button(self.frm_action, text="Add merge dice feature")
        self.btn_add_buy_shop_feature = tk.Button(self.frm_action, text="Add buy shop feature")
        self.btn_add_buy_dice_feature = tk.Button(self.frm_action, text="Add buy dice feature")
        self.btn_start = tk.Button(self.frm_action, text="Start bot")

        self.btn_add_merge_dice_feature['command'] = \
            lambda: self.add_feature(MergeDiceFeatureView(self.frm_feature, deck=self.deck))
        self.btn_add_buy_shop_feature['command'] = \
            lambda: self.add_feature(BuyUpgradeFeatureView(self.frm_feature, deck=self.deck))
        self.btn_add_buy_dice_feature['command'] = \
            lambda: self.add_feature(BuyDiceFeatureView(self.frm_feature))
        self.btn_start['command'] = \
            lambda: self.set_show(False)

        # frm_action widgets layouts
        self.btn_add_merge_dice_feature.grid(row=0, column=0)
        self.btn_add_buy_shop_feature.grid(row=1, column=0)
        self.btn_add_buy_dice_feature.grid(row=2, column=0)
        self.btn_start.grid(row=4, column=0)

        # load all dices images
        self.all_dice_images = {}
        for name, member in DiceColorEnum.__members__.items():
            image = Image.open("../image/dice/%s.png" % name)
            image = image.resize((50, 50), Image.ANTIALIAS)
            self.all_dice_images[member] = ImageTk.PhotoImage(image)

    def update_image_dices(self):
        """
        Update images in the ui with the current dice deck
        """
        for idx, dice_canvas in enumerate(self.dices_canvas):
            dice_canvas.delete("all")
            dice_canvas.create_image(0, 0, anchor="nw",
                                     image=self.all_dice_images[self.deck.dices[idx]])
        self.deck.notify()

    def change_dice_dialog(self, index_dice_deck):
        """
        Open the SelectDiceDialog for change a dice
        """
        new = tk.Toplevel(self.root)
        new.grab_set()
        SelectDiceDialog(new, self, index_dice_deck)

    def update_frm_feature(self):
        for idx, sub_feature_frm in enumerate(self.sub_feature_frms):
            sub_feature_frm.get_frm().grid_forget()
            sub_feature_frm.get_frm().grid(row=idx, column=0)

    def add_feature(self, feature_view):
        self.sub_feature_frms.append(feature_view)
        self.update_frm_feature()
        self.update_image_dices()

    def set_show(self, value: bool):
        self.show = value

    def show_dialog(self):
        """Show this dialog"""
        self.root.deiconify()
        self.show = True
        while self.show:
            self.root.update_idletasks()
            self.root.update()
        self.root.withdraw()
        return self


class SelectDiceDialog:
    """Select one dice of all dice"""

    def __init__(self, root, main_dialog: MainDialog, index_dice_deck):
        self.root = root
        # self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.main_dialog = main_dialog
        self.index_dice_deck = index_dice_deck

        # widgets
        self.lst_dices = self.lst_dices = tk.Listbox(self.root, width=20, height=10)
        for name, member in DiceColorEnum.__members__.items():
            self.lst_dices.insert(tk.END, name)
        self.btn_selectionner = tk.Button(self.root, text="Selectionnner", command=lambda: self.callback_selectionner())
        # layout widgets
        self.lst_dices.pack()
        self.btn_selectionner.pack()

    def callback_selectionner(self):
        for index in self.lst_dices.curselection():
            type_dice = DiceColorEnum[self.lst_dices.get(index)]

            flag_dice_already_in_deck = False
            idx_dice = 0
            for idx, dice in enumerate(self.main_dialog.deck.dices):
                if dice == type_dice:
                    flag_dice_already_in_deck = True
                    idx_dice = idx
                    break

            if flag_dice_already_in_deck:
                self.main_dialog.deck.dices[idx_dice] = self.main_dialog.deck.dices[self.index_dice_deck]
                self.main_dialog.deck.dices[self.index_dice_deck] = type_dice
            else:
                self.main_dialog.deck.dices[self.index_dice_deck] = type_dice

            self.main_dialog.update_image_dices()
            self.root.destroy()


class AbstractFeatureView:
    def __init__(self, root):
        self.root = root

        # Frame
        self.frm = tk.Frame(self.root, width=2, height=1)
        self.frm_lbl = tk.Frame(self.frm, width=2, height=1)
        self.frm_option = tk.Frame(self.frm, width=2, height=1)

        # Frame grid
        self.frm_lbl.pack()
        self.frm_option.pack()

        # frm widgets
        self.lbl_name_feature = tk.Label(self.frm_lbl, text="default", anchor="w", font='Helvetica 12 bold')
        self.lbl_name_custom = tk.Label(self.frm_lbl, anchor="w")

        # frm widgets layout
        self.lbl_name_feature.grid(row=0, column=0)
        self.lbl_name_custom.grid(row=0, column=1)

        # parameters
        self.parameters = None

    @abstractmethod
    def get_frm(self):
        pass

    @abstractmethod
    def get_callback_feature(self):
        pass


class MergeDiceFeatureView(AbstractFeatureView):
    """Merge dice"""

    def __init__(self, root, deck: Deck, parameters: Optional[Dict] = None):
        super().__init__(root)
        self.deck = deck

        # change name label
        self.lbl_name_feature['text'] = "Merge dice"

        # widgets
        # dices
        self.lbx_dices_value = tk.StringVar()

        # config
        self.btn_config = tk.Button(self.frm_option, width=8, text="Config")
        self.btn_config['command'] = self.callback_config
        self.btn_config.pack()

        # default parameters
        if parameters is not None:
            self.parameters = parameters
        else:
            self.parameters = {
                "name": "",
                "lst_from": [],
                "lst_to": [],
                "min_dices_board": 2,
                "max_dices_board": 15,
                "min_dots": 1,
                "max_dots": 7,
                "min_dices_from": 1,
                "min_dices_to": 1,
                "merge_priority": 1,
            }

        self.lbl_name_custom['text'] = self.parameters.get('name')

    def callback_config(self):
        self.parameters = DiceMergeFeatureConfDialog(self.deck, True, self.parameters).returning
        self.lbl_name_custom['text'] = self.parameters.get('name')

    def get_frm(self):
        return self.frm

    def get_callback_feature(self):
        return lambda plateau: merge_dice_feature(
            plateau,
            self.parameters.get('lst_from'),
            self.parameters.get('lst_to'),
            self.parameters.get('min_dices_board'),
            self.parameters.get('max_dices_board'),
            self.parameters.get('min_dots'),
            self.parameters.get('max_dots'),
            self.parameters.get('min_dices_from'),
            self.parameters.get('min_dices_to'),
            self.parameters.get('merge_priority') == 1,
        )


class BuyUpgradeFeatureView(AbstractFeatureView):
    """Buy upgrade"""

    def __init__(self, root, deck: Deck, parameters: Optional[Dict] = None):
        super().__init__(root)
        self.deck = deck

        # change name label
        self.lbl_name_feature['text'] = "Buy upgrade"

        # config
        self.btn_config = tk.Button(self.frm_option, width=8, text="Config")
        self.btn_config['command'] = self.callback_config
        self.btn_config.pack()

        # default parameters
        if parameters is not None:
            self.parameters = parameters
        else:
            self.parameters = {
                "name": "",
                "lst_index_dice": [],
                "proba_buy_upgrade": 0.05,
                "min_dices_board": 8,
            }

        self.lbl_name_custom['text'] = self.parameters.get('name')

    def callback_config(self):
        self.parameters = BuyUpgradeFeatureConfDialog(self.deck, True, self.parameters).returning
        self.lbl_name_custom['text'] = self.parameters.get('name')

    def get_frm(self):
        return self.frm

    def get_callback_feature(self):
        return lambda plateau: buy_upgrade_feature(
            plateau,
            self.parameters.get('proba_buy_upgrade'),
            self.parameters.get('lst_index_dice'),
            self.parameters.get('min_dices_board'),
        )


class BuyDiceFeatureView(AbstractFeatureView):
    """Buy dice"""

    def __init__(self, root):
        super().__init__(root)

        # change name label
        self.lbl_name_feature['text'] = "Buy dice"

    def get_frm(self):
        return self.frm

    def get_callback_feature(self):
        return lambda plateau: buy_dice_feature(plateau)


# root = tk.Tk()
# ahk = AHK()
# # plateau = Plateau(ahk)
#
# main_dialog = MainDialog(root)
# main_dialog.update_image_dices()
# main_dialog.update_frm_feature()
#
# root.mainloop()
