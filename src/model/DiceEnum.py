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


from enum import Enum

# 47 Dices
class DiceEnum(Enum):
    FIRE = 0
    ELECTRIC = 1
    WIND = 2
    POISON = 3
    ICE = 4
    IRON = 5
    BROKEN = 6
    GAMBLE = 7
    LOCK = 8
    MINE = 9
    LIGHT = 10
    THORN = 11
    CRACK = 12
    CRITICAL = 13
    ENERGY = 14
    SACRIFICIAL = 15
    BOW = 16
    DEATH = 17
    TELEPORT = 18
    LASER = 19
    MIMIC = 20
    INFECT = 21
    MODIFIED_ELECTRIC = 22
    ABSORB = 23
    MIGHTY_WIND = 24
    SWITCH = 25
    GEAR = 26
    WAVE = 27
    NUCLEAR = 28
    LANDMINE = 29
    SAND_SWAMP = 30
    JOKER = 31
    HOLY8SWORD = 32
    HELL = 33
    SHIELD = 34
    BLIZZARD = 35
    GROWTH = 36
    SUMMONER = 37
    SOLAR = 38
    ASSASSIN = 39
    GUN = 40
    ELEMENT = 41
    SUPPLEMENT = 42
    METASTASIS = 43
    TYPHOON = 44
    TIME = 45
    COMBO = 46


class DiceColorEnum(Enum):
    FIRE = (0, [(48, 39, 210)])
    ELECTRIC = (1, [(15, 177, 254)])
    WIND = (2, [(162, 201, 1)])
    POISON = (3, [(28, 191, 45)])
    ICE = (4, [(243, 145, 61)])
    IRON = (5, [(177, 177, 177)])
    BROKEN = (6, [(251, 8, 143)])
    GAMBLE = (7, [(255, 8, 90)])
    LOCK = (8, [(74, 75, 75)])
    MINE = (9, [(251, 232, 1)])
    LIGHT = (10, [])
    THORN = (11, [(0, 0, 0)])
    CRACK = (12, [(0, 0, 0)])
    CRITICAL = (13, [])
    ENERGY = (14, [(205, 234, 27)])
    SACRIFICIAL = (15, [(235, 34, 60)])
    BOW = (16, [(0, 0, 0)])

    MIMIC = (20, [])

    JOKER = (31, [])

    GROWTH = (36, [(147, 40, 57), (119, 29, 46)])

    COMBO = (46, [(145, 32, 162)])

    METASTASIS =(43, [(108, 35, 73)])