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
from typing import Optional

from src.view.Deck import Deck
from src.view.Observer import Observer, Observable


class ListDice(Observer):
    """
    A widget list where you can select dices from a specific Deck
    """
    def __init__(self, root, deck: Deck, lbl_text: str, dices_index_selected: Optional[list]):
        self.root = root
        self.deck = deck
        self.lbl_text = lbl_text

        # Frame
        self.frm = tk.Frame(self.root, width=2, height=60)

        # widgets
        self.lbl = tk.Label(self.frm, text=self.lbl_text, anchor="w")
        self.lst_dices = tk.Listbox(self.frm, selectmode=tk.MULTIPLE, exportselection=0, width=20, height=5)
        self.update(deck)
        for idx_dices in dices_index_selected:
            self.lst_dices.select_set(idx_dices)

        # widgets layouts
        self.lbl.pack()
        self.lst_dices.pack()

    def get_selected_dices(self):
        return [self.deck.dices[idx_dice_deck] for idx_dice_deck in self.lst_dices.curselection()]

    def update(self, observable: Observable) -> None:
        assert isinstance(observable, Deck)

        self.lst_dices.delete(0, tk.END)
        for dice in observable.dices:
            self.lst_dices.insert(tk.END, dice.name)


class FieldInt:
    """
    A int field + label with min/max.
    """
    def __init__(self, root, lbl_text: str, min_value: int, default_value: int, max_value: int):
        assert min_value <= default_value <= max_value

        self.root = root
        self.lbl_text = lbl_text
        self.min_value = min_value
        self.default_value = default_value
        self.max_value = max_value

        # Frame
        self.frm = tk.Frame(self.root)

        # widgets
        self.lbl = tk.Label(self.frm, text=self.lbl_text, anchor="w")
        self.entry_var = tk.IntVar(self.frm, default_value)
        self.entry = tk.Entry(self.frm, textvariable=self.entry_var)

        # widgets layouts
        self.lbl.grid(row=0, column=0)
        self.entry.grid(row=0, column=1)

    def get_value(self):
        value = self.entry_var.get()
        if value < self.min_value:
            return self.min_value
        elif value > self.max_value:
            return self.max_value
        return value


class FieldString:
    """
    A str field + label.
    """
    def __init__(self, root, lbl_text: str, default_value: str):
        self.root = root
        self.lbl_text = lbl_text
        self.default_value = default_value

        # Frame
        self.frm = tk.Frame(self.root)

        # widgets
        self.lbl = tk.Label(self.frm, text=self.lbl_text, anchor="w")
        self.entry_var = tk.StringVar(self.frm, default_value)
        self.entry = tk.Entry(self.frm, textvariable=self.entry_var)

        # widgets layouts
        self.lbl.grid(row=0, column=0)
        self.entry.grid(row=0, column=1)

    def get_value(self):
        value = self.entry_var.get()
        return value


class FieldRadioBinary:
    """
    2 radio buttons, like a check box
    """
    def __init__(self, root, lbl_main: str, lbl1: str, lbl2: str, default: int):
        self.root = root
        self.lbl_main_text = lbl_main
        self.lbl1_text = lbl1
        self.lbl2_text = lbl2

        # Frame
        self.frm = tk.Frame(self.root)

        # widgets
        self.lbl_main = tk.Label(self.frm, text=self.lbl_main_text, anchor="w")

        self.radio_val = range(2)  # 0 = first, 1 = second
        self.radio_etiqs = [self.lbl1_text, self.lbl2_text]
        self.radio_varGr = tk.IntVar(self.frm, self.radio_val[default-1])
        self.radios = []
        for i in range(2):
            b = tk.Radiobutton(self.frm,
                               variable=self.radio_varGr,
                               text=self.radio_etiqs[i],
                               value=self.radio_val[i])
            self.radios.append(b)

        # widgets layouts
        self.lbl_main.grid(row=0, column=0)
        self.radios[0].grid(row=0, column=2)
        self.radios[1].grid(row=0, column=4)

    def get_value(self):
        """
        :return: 1 or 2
        """
        return self.radio_varGr.get() + 1
