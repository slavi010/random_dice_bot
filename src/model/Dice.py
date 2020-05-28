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


from src.model.DiceEnum import DiceEnum, DiceColorEnum


class Dice:
    def __init__(self, type_dice: DiceColorEnum, dot: int):
        if not is_valid_dot_dice(dot):
            raise Exception('Out of valid dot range : (' + str(dot) + ')')

        self.type_dice = type_dice
        self.dot = dot

    def __str__(self):
        return self.type_dice.name + " " + str(self.dot)


def is_valid_dot_dice(dot: int):
    """Return a boolean if if valid dot range"""
    return 0 < dot <= 7
