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
from tkinter import ttk

import cv2
import numpy as np
from PIL import ImageTk, Image

from src.model.DiceEnum import DiceColorEnum


class MainDialog:
    """The main Dialog, with this dialog, you can change the deck and the bot actions"""

    def __init__(self, root):
        self.root = root

        # Frame
        self.frm_deck = tk.Frame(self.root, width=300, height=60, pady=3)
        # self.frm_feature = tk.Frame(self.root, width=300, height=60, pady=3)

        # Frame grid
        self.frm_deck.grid(row=0, sticky="ew")
        # self.frm_feature.grid(row=1, sticky="ew")

        # frm_deck widgets
        self.dices = [DiceColorEnum.JOKER, DiceColorEnum.GROWTH, DiceColorEnum.MIMIC, DiceColorEnum.SACRIFICIAL,
                      DiceColorEnum.COMBO]
        self.dices_canvas = []
        for i in range(5):
            canvas = tk.Canvas(self.frm_deck, width=50, height=50)
            self.dices_canvas.append(canvas)
        self.dices_canvas[0].bind("<Button-1>", self.callback_change_dice_1)
        self.dices_canvas[1].bind("<Button-1>", self.callback_change_dice_2)
        self.dices_canvas[2].bind("<Button-1>", self.callback_change_dice_3)
        self.dices_canvas[3].bind("<Button-1>", self.callback_change_dice_4)
        self.dices_canvas[4].bind("<Button-1>", self.callback_change_dice_5)

        # frm_deck layout widgets
        for idx, dice_canvas in enumerate(self.dices_canvas):
            dice_canvas.grid(row=0, column=idx)

        # frm_feature widgets
        # self.sub_feature_frms = []

        # load all dices images
        self.all_dice_images = {}
        for name, member in DiceColorEnum.__members__.items():
            image = Image.open("../../image/dice/%s.png" % name)
            image = image.resize((50, 50), Image.ANTIALIAS)
            self.all_dice_images[member] = ImageTk.PhotoImage(image)

    def update_image_dices(self):
        """update the image in the window with the current dice deck"""
        for idx, dice_canvas in enumerate(self.dices_canvas):
            dice_canvas.delete("all")
            dice_canvas.create_image(0, 0, anchor="nw",
                                     image=self.all_dice_images[self.dices[idx]])

    def callback_change_dice_1(self, event):
        self.change_dice_dialog(0)

    def callback_change_dice_2(self, event):
        self.change_dice_dialog(1)

    def callback_change_dice_3(self, event):
        self.change_dice_dialog(2)

    def callback_change_dice_4(self, event):
        self.change_dice_dialog(3)

    def callback_change_dice_5(self, event):
        self.change_dice_dialog(4)

    def change_dice_dialog(self, index_dice_deck):
        new = tk.Toplevel(self.root)
        new.grab_set()
        SelectDiceDialog(new, self, index_dice_deck)


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
            for idx, dice in enumerate(self.main_dialog.dices):
                if dice == type_dice:
                    flag_dice_already_in_deck = True
                    idx_dice = idx
                    break

            if flag_dice_already_in_deck:
                self.main_dialog.dices[idx_dice] = self.main_dialog.dices[self.index_dice_deck]
                self.main_dialog.dices[self.index_dice_deck] = type_dice
            else:
                self.main_dialog.dices[self.index_dice_deck] = type_dice

            self.main_dialog.update_image_dices()
            self.root.destroy()


# class AbstractFeatureView()


root = tk.Tk()
main_dialog = MainDialog(root)
main_dialog.update_image_dices()

root.mainloop()
