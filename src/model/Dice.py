#################################################################################
# THE isinstance(SOFTWARE, PROVIDED) "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR    #
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
from typing import Union

from src.model.DiceEnum import DiceEnum, DiceColorEnum


class Dice:
    def __init__(self, type_dice: DiceColorEnum, dot: int):
        if not is_valid_dot_dice(dot):
            raise Exception('Out of valid dot range : (' + str(dot) + ')')

        self.type_dice = type_dice
        self.dot = dot

    def __lt__(self, other):
        """Return True if :
            other is a Dice and they have the same type and self.dot < other.dot.
            other is int and self.dot < other
        """
        if isinstance(other, int):
            return self.dot < other
        elif isinstance(other, Dice):
            return self.type_equal(other) and self.dot < other.dot
        else:
            raise AssertionError("other is not a Dice or a int")

    def __le__(self, other):
        """Return True if :
            other is a Dice and they have the same type and self.dot <= other.dot.
            other is int and self.dot <= other
        """
        if isinstance(other, int):
            return self.dot <= other
        elif isinstance(other, Dice):
            return self.type_equal(other) and self.dot <= other.dot
        else:
            raise AssertionError("other is not a Dice or a int")

    def __eq__(self, other):
        """Return True if :
            other is a Dice and they have the same type and dot.
            other is DiceColorEnum and self.type_dice == other.
            other is int and self.dot == other.
            other is a tuple or a list, and if one item matches with this description recursively.
        """
        if isinstance(other, tuple) or isinstance(other, list):
            for item in other:
                if self.__eq__(item) is True:
                    return True
            return False
        else:
            return self.equal(other)

    def equal(self, other):
        """Return True if :
            other is a Dice and they have the same type and dot.
            other is DiceColorEnum and self.type_dice == other.
            other is int and self.dot == other
        """
        if isinstance(other, int):
            return self.dot == other
        elif isinstance(other, Dice):
            return self.type_equal(other) and self.dot == other.dot
        elif isinstance(other, DiceColorEnum):
            return self.type_dice == other
        else:
            raise AssertionError("other is not a Dice, a DiceColorEnum or a int")

    def __ne__(self, other):
        """Return True if :
            other is a Dice and they have not the same type or dot.
            other is DiceColorEnum and self.type_dice != other.
            other is int and self.dot != other.
            other is a tuple or a list, and if all items matches with this description recursively.
        """
        return not self.__eq__(other)

    def __gt__(self, other):
        """Return True if :
            other is a Dice and they have the same type and self.dot > other.dot.
            other is int and self.dot > other
        """
        if isinstance(other, int):
            return self.dot > other
        elif isinstance(other, Dice):
            return self.type_equal(other) and self.dot > other.dot
        else:
            raise AssertionError("other is not a Dice or a int")

    def __ge__(self, other):
        """Return True if :
            other is a Dice and they have the same type and self.dot >= other.dot.
            other is int and self.dot >= other
        """
        if isinstance(other, int):
            return self.dot >= other
        elif isinstance(other, Dice):
            return self.type_equal(other) and self.dot >= other.dot
        else:
            raise AssertionError("other is not a Dice or a int")

    def type_equal(self, other):
        """Return True if other is a Dice and they have the same type"""
        assert isinstance(other, Dice)

        return self.type_dice == other.type_dice

    def __str__(self):
        return self.type_dice.name + " " + str(self.dot)


def is_valid_dot_dice(dot: int):
    """Return a boolean if if valid dot range"""
    return 0 < dot <= 7
